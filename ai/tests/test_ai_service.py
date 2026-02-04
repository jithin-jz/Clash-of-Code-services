import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from auto_generator import AutoGenerator, ChallengeSchema

# Mock Data
MOCK_CHALLENGE_JSON = """
{
    "title": "Test Challenge",
    "description": "Test Description",
    "initial_code": "# code",
    "test_code": "def test_solution(): pass",
    "reference_solution": "def solution(): pass",
    "hint": "Try harder",
    "slug": "test-challenge"
}
"""

@pytest.fixture
def mock_llm_chain():
    with patch("auto_generator.LLMFactory") as MockFactory:
        mock_llm = MagicMock()
        MockFactory.get_llm.return_value = mock_llm
        
        # Mock the chain execution
        # complex mocking because of chain | pipe syntax
        # simpler to mock AutoGenerator.parser or the chain.ainvoke directly if possible
        # but since chain is constructed inside, we might need to mock LLMFactory to return a mock that produces expected Pydantic object
        yield MockFactory

@pytest.mark.asyncio
async def test_challenge_schema_validation():
    """Verify that ChallengeSchema accepts valid data"""
    data = {
        "title": "Valid Title",
        "description": "Desc",
        "initial_code": "print('hello')",
        "test_code": "assert True",
        "reference_solution": "print('hello')",
        "hint": "hint",
        "slug": "valid-slug"
    }
    schema = ChallengeSchema(**data)
    assert schema.title == "Valid Title"

@pytest.mark.asyncio
async def test_auto_generator_initialization():
    """Verify AutoGenerator initializes parser"""
    gen = AutoGenerator()
    assert gen.parser is not None

# Note: Full integration testing of generate_level requires more complex mocking of the LangChain pipeline
# intended for the next step.
