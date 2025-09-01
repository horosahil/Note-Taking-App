from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List
from .database import db, settings
from .schemas import NoteCreate, NoteUpdate, NotePublic
from .models import NoteDB, UserDB
from .utils import decode_jwt

router = APIRouter(prefix="/api/notes", tags=["notes"])

def current_user_id(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    data = decode_jwt(token, settings.JWT_SECRET)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return data.get("sub")

@router.get("/", response_model=List[NotePublic])
async def list_notes(request: Request):
    user_id = current_user_id(request)
    cursor = db.notes.find({"user_id": user_id}).sort("last_update", -1)
    results = []
    async for doc in cursor:
        note = NoteDB(**doc)
        results.append(NotePublic(
            note_id=note.note_id,
            note_title=note.note_title,
            note_content=note.note_content,
            created_on=note.created_on,
            last_update=note.last_update
        ))
    return results

@router.post("/", response_model=NotePublic, status_code=201)
async def create_note(payload: NoteCreate, request: Request):
    user_id = current_user_id(request)
    note = NoteDB(user_id=user_id, note_title=payload.note_title, note_content=payload.note_content)
    await db.notes.insert_one(note.model_dump())
    return NotePublic(**note.model_dump())

@router.get("/{note_id}", response_model=NotePublic)
async def get_note(note_id: str, request: Request):
    user_id = current_user_id(request)
    doc = await db.notes.find_one({"note_id": note_id, "user_id": user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Note not found")
    note = NoteDB(**doc)
    return NotePublic(**note.model_dump())

@router.put("/{note_id}", response_model=NotePublic)
async def update_note(note_id: str, payload: NoteUpdate, request: Request):
    user_id = current_user_id(request)
    doc = await db.notes.find_one({"note_id": note_id, "user_id": user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Note not found")
    changes = {}
    if payload.note_title is not None:
        changes["note_title"] = payload.note_title
    if payload.note_content is not None:
        changes["note_content"] = payload.note_content
    if not changes:
        return doc
    changes["last_update"] = __import__("datetime").datetime.utcnow()
    await db.notes.update_one({"note_id": note_id, "user_id": user_id}, {"$set": changes})
    doc = await db.notes.find_one({"note_id": note_id, "user_id": user_id})
    return NotePublic(**doc)

@router.delete("/{note_id}", status_code=204)
async def delete_note(note_id: str, request: Request):
    user_id = current_user_id(request)
    res = await db.notes.delete_one({"note_id": note_id, "user_id": user_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return