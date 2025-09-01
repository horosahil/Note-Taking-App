from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# Request/Response schemas

class UserCreate(BaseModel):
    user_name: str
    user_email: EmailStr
    password: str

class UserLogin(BaseModel):
    user_email: EmailStr
    password: str

class UserPublic(BaseModel):
    user_id: str
    user_name: str
    user_email: EmailStr
    created_on: datetime
    last_update: datetime

class NoteCreate(BaseModel):
    note_title: str
    note_content: str

class NoteUpdate(BaseModel):
    note_title: Optional[str] = None
    note_content: Optional[str] = None

class NotePublic(BaseModel):
    note_id: str
    note_title: str
    note_content: str
    created_on: datetime
    last_update: datetime