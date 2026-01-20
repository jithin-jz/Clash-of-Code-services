from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException, status
from typing import List, Dict
import os
import json
import jwt
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="CodeShorts Chat Service")

# --- Configuration ---
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-from-backend") # MUST MATCH CORE BACKEND
ALGORITHM = "HS256"

# --- Redis Config ---
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
import redis
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
CHAT_HISTORY_KEY = "chat:history:global"

# --- Manager ---
class ConnectionManager:
    def __init__(self):
        # Store active connections: room_name -> List[WebSocket]
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_name: str):
        await websocket.accept()
        if room_name not in self.active_connections:
            self.active_connections[room_name] = []
        self.active_connections[room_name].append(websocket)
        
        # Send history on connect
        history = redis_client.lrange(CHAT_HISTORY_KEY, 0, 49)
        if history:
             # Redis stores text, parse it back to JSON
            parsed_history = [json.loads(msg) for msg in history]
            # Reverse because lrange gives oldest first if we pushed right?
            # Wait, rpush adds to tail. lrange(0, -1) gets head to tail.
            # Messages: [Msg1, Msg2, Msg3] -> lrange gives [Msg1, Msg2, Msg3].
            # Frontend appends new messages.
            # So sending them in order [oldest ... newest] is correct.
            
            await websocket.send_text(json.dumps({
                "type": "history",
                "messages": parsed_history
            }))

    def disconnect(self, websocket: WebSocket, room_name: str):
        if room_name in self.active_connections:
            if websocket in self.active_connections[room_name]:
                self.active_connections[room_name].remove(websocket)
            if not self.active_connections[room_name]:
                del self.active_connections[room_name]

    async def broadcast(self, message: dict, room_name: str):
        # Save to Redis
        redis_client.rpush(CHAT_HISTORY_KEY, json.dumps(message))
        redis_client.ltrim(CHAT_HISTORY_KEY, -50, -1) # Keep last 50

        if room_name in self.active_connections:
            # Serializing once to save time
            text_data = json.dumps(message)
            for connection in self.active_connections[room_name]:
                try:
                    await connection.send_text(text_data)
                except:
                    # Handle dead connections
                    pass

manager = ConnectionManager()

# --- Auth Helper ---
def verify_token(token: str):
    """
    Decodes the JWT token issued by the Core Django App.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            return None
        return payload
    except jwt.PyJWTError:
        return None

# --- Routes ---

@app.get("/")
def read_root():
    return {"status": "Chat Service Running"}

@app.websocket("/ws/chat/{room_name}/")
async def websocket_endpoint(websocket: WebSocket, room_name: str, token: str = Query(...)):
    """
    WebSocket endpoint for chat.
    Requires a valid JWT token in the query parameter '?token=...'
    """
    user_payload = verify_token(token)
    
    if not user_payload:
        # Close with policy violation code if auth fails
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # In a real app, you might fetch user name from payload or DB
    # For now, we assume payload has 'username' or we use user_id
    # Django SimpleJWT users usually put 'user_id' in payload. 
    # You might need to add custom claims in Django to include username.
    user_id = user_payload.get("user_id")
    username = user_payload.get("username", f"User {user_id}")
    
    await manager.connect(websocket, room_name)
    
    try:
        while True:
            data = await websocket.receive_text()
            # Expecting JSON input
            try:
                message_data = json.loads(data)
                logger_msg = message_data.get("message", "")
                
                # Construct response
                response = {
                    "type": "chat_message",
                    "message": logger_msg,
                    "user_id": user_id,
                    "username": username,
                    "sender": username,
                    "avatar_url": user_payload.get("avatar_url") # Optional: if we add avatar later
                }
                
                await manager.broadcast(response, room_name)
            except json.JSONDecodeError:
                pass
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_name)
        # Optional: Broadcast "User left" message
