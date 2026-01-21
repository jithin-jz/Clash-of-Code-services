from pydantic import BaseModel, Field
from typing import Literal, Optional
import time
import uuid


class BaseEvent(BaseModel):
    type: str
    timestamp: int = Field(default_factory=lambda: int(time.time()))


class ChatMessage(BaseEvent):
    type: Literal["chat_message"] = "chat_message"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    room: str
    message: str = Field(min_length=1, max_length=1000)
    user_id: int
    username: str


class PresenceEvent(BaseEvent):
    type: Literal["presence"] = "presence"
    event: Literal["join", "leave"]
    user_id: int
    username: str


class IncomingMessage(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
