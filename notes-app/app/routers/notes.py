from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models
from app.auth import get_current_user
from app.dependencies import get_db
from app.schemas.note import NoteCreate, NoteResponse

router = APIRouter()


@router.post("/notes", response_model=NoteResponse)
async def create_note(
    note: NoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_note = models.Note(**note.dict(), user_id=current_user.id)
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note


@router.get("/notes", response_model=List[NoteResponse])
async def get_notes(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    result = await db.execute(select(models.Note).filter(models.Note.user_id == current_user.id))
    notes = result.scalars().all()
    return notes


@router.get("/notes/{id}", response_model=NoteResponse)  # Usamos NoteResponse aquí
async def get_note_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(select(models.Note).filter(models.Note.id == id, models.Note.user_id == current_user.id))
    note = result.scalar_one_or_none()  # Obtener la primera nota o None
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/notes/{id}", response_model=NoteResponse)
async def update_note(
    id: int,
    note: NoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(select(models.Note).filter(models.Note.id == id, models.Note.user_id == current_user.id))
    db_note = result.scalar_one_or_none()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    db_note.title = note.title
    db_note.content = note.content

    await db.commit()
    await db.refresh(db_note)
    return db_note



@router.delete("/notes/{id}", response_model=NoteResponse)
async def delete_note(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(select(models.Note).filter(models.Note.id == id, models.Note.user_id == current_user.id))
    db_note = result.scalar_one_or_none()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    await db.delete(db_note)
    await db.commit()
    return db_note
