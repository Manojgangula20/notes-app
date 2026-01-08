from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_db_dep, get_current_user
from app.models.note import Note
from app.models.user import User
from app.models.version import NoteVersion
from app.schemas.note import NoteCreate, NoteUpdate, NoteOut

router = APIRouter(prefix="/notes", tags=["notes"])


def get_note_or_404(note_id: int, user: User, db: Session) -> Note:
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.owner_id == user.id)
        .first()
    )
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )
    return note


@router.post(
    "",
    response_model=NoteOut,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    note_in: NoteCreate,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_user),
):
    note = Note(
        title=note_in.title,
        content=note_in.content,
        owner_id=current_user.id,
    )
    db.add(note)
    db.flush()  # get note.id before commit

    version = NoteVersion(
        note_id=note.id,
        version=1,
        content=note.content,
        editor_id=current_user.id,
    )
    db.add(version)
    db.commit()
    db.refresh(note)
    return note


@router.get("", response_model=List[NoteOut])
def list_notes(
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_user),
):
    notes = (
        db.query(Note)
        .filter(Note.owner_id == current_user.id)
        .order_by(Note.created_at.desc())
        .all()
    )
    return notes


@router.get("/{note_id}", response_model=NoteOut)
def get_note(
    note_id: int,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_user),
):
    note = get_note_or_404(note_id, current_user, db)
    return note


@router.put("/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int,
    note_in: NoteUpdate,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_user),
):
    note = get_note_or_404(note_id, current_user, db)

    if note_in.title is not None:
        note.title = note_in.title
    if note_in.content is not None:
        note.content = note_in.content

    # compute next version number
    max_version = (
        db.query(func.max(NoteVersion.version))
        .filter(NoteVersion.note_id == note.id)
        .scalar()
        or 0
    )
    new_version_num = max_version + 1

    version = NoteVersion(
        note_id=note.id,
        version=new_version_num,
        content=note.content,
        editor_id=current_user.id,
    )

    db.add(version)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_user),
):
    note = get_note_or_404(note_id, current_user, db)
    db.delete(note)
    db.commit()
    return None
