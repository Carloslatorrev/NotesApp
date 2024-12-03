from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.note import Note
from app.schemas.note import NoteCreate


async def get_all_notes(session: AsyncSession):
    result = await session.execute(select(Note))
    return result.scalars().all()


async def create_note(session: AsyncSession, note_data: NoteCreate):
    new_note = Note(**note_data.dict())
    session.add(new_note)
    await session.commit()
    await session.refresh(new_note)
    return new_note
