from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import uuid4

def now_utc() -> datetime:
    return datetime.utcnow()

# Database models (as dicts for Mongo)

class UserDB(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid4()))
    user_name: str
    user_email: EmailStr
    password_hash: str
    created_on: datetime = Field(default_factory=now_utc)
    last_update: datetime = Field(default_factory=now_utc)

class NoteDB(BaseModel):
    note_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    note_title: str
    note_content: str
    created_on: datetime = Field(default_factory=now_utc)
    last_update: datetime = Field(default_factory=now_utc)