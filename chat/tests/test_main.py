import os
import pytest

# Set dummy environment variables BEFORE importing main app
os.environ["DATABASE_URL"] = "postgresql+asyncpg://user:pass@localhost/db"
os.environ["REDIS_URL"] = "redis://localhost:6379/0"
os.environ["JWT_PUBLIC_KEY"] = "dummy_key"

import jwt
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "chat"}


def test_history_no_token():
    response = client.get("/history/general")
    assert response.status_code == 401
    assert response.json()["error"] == "Invalid token"


@patch("main.verify_jwt")
def test_history_invalid_token(mock_verify):
    mock_verify.return_value = None
    response = client.get(
        "/history/general", headers={"Authorization": "Bearer invalid"}
    )
    assert response.status_code == 401
    assert response.json()["error"] == "Invalid token"


@pytest.mark.asyncio
@patch("main.verify_jwt")
@patch("main.dynamo_client")
async def test_history_success_dynamo(mock_dynamo, mock_verify):
    # Setup mocks
    mock_verify.return_value = {"user_id": 1, "username": "testuser"}
    mock_dynamo.get_messages = AsyncMock(
        return_value=[
            {
                "sender": "user1",
                "content": "hello",
                "timestamp": "2023-01-01T00:00:00",
                "reactions": {},
            }
        ]
    )

    # We use TestClient which is synchronous, but the endpoint is async.
    # TestClient handles async endpoints internally by running them in an event loop.
    response = client.get("/history/general", headers={"Authorization": "Bearer valid"})

    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "dynamodb"
    assert len(data["messages"]) == 1
    assert data["messages"][0]["message"] == "hello"


@pytest.mark.asyncio
@patch("main.verify_jwt")
@patch("main.dynamo_client")
@patch("main.sessionmaker")
async def test_history_fallback_to_sql(mock_sessionmaker, mock_dynamo, mock_verify):
    mock_verify.return_value = {"user_id": 1, "username": "testuser"}

    # DynamoDB is empty
    mock_dynamo.get_messages = AsyncMock(return_value=[])

    # Mock SQL Session
    mock_session = AsyncMock()
    # Mock aenter/aexit for 'async with async_session() as session'
    mock_sessionmaker.return_value.return_value.__aenter__.return_value = mock_session

    # Mock SQL result
    mock_msg = MagicMock()
    mock_msg.username = "sqluser"
    mock_msg.message = "sql message"
    mock_msg.timestamp.isoformat.return_value = "2023-01-01T00:00:00"
    mock_msg.reactions = {}

    mock_scalars = MagicMock()
    mock_scalars.all.return_value = [mock_msg]

    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars

    mock_session.execute.return_value = mock_result

    response = client.get("/history/general", headers={"Authorization": "Bearer valid"})

    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "sql"
    assert data["messages"][0]["username"] == "sqluser"
    assert data["messages"][0]["message"] == "sql message"
