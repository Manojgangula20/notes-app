from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_db_dep, get_current_user
from app.models.note import Note
from app.models.user import User
from app.models.version import NoteVersion
from app.schemas.version import VersionOut

router = APIRouter(prefix="/notes", tags=["versions"])


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


def get_version_or_404(note_id: int, version: int, db: Session) -> NoteVersion:
    version_obj = (
        db.query(NoteVersion)
        .filter(
            NoteVersion.note_id == note_id,
            NoteVersion.version == version,
        )
        .first()
    )
    if not version_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Version not found",
        )
    return version_obj


@router.get("/{note_id}/versions", response_model=List[VersionOut])
def list_versions(
    note_id: int,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_user),
):
    note = get_note_or_404(note_id, current_user, db)

    versions = (
        db.query(NoteVersion)
        .filter(NoteVersion.note_id == note.id)
        .order_by(NoteVersion.version.asc())
        .all()
    )
    return versions


@router.get("/{note_id}/versions/{version}", response_model=VersionOut)
def get_version(
    note_id: int,
    version: int,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_user),
):
    note = get_note_or_404(note_id, current_user, db)
    version_obj = get_version_or_404(note.id, version, db)
    return version_obj


@router.post(
    "/{note_id}/versions/{version}/restore",
    response_model=VersionOut,
)
def restore_version(
    note_id: int,
    version: int,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_user),
):
    note = get_note_or_404(note_id, current_user, db)
    version_to_restore = get_version_or_404(note.id, version, db)

    # Update note content to the version's snapshot
    note.content = version_to_restore.content

    # Create a new version representing this restore action
    max_version = (
        db.query(func.max(NoteVersion.version))
        .filter(NoteVersion.note_id == note.id)
        .scalar()
        or 0
    )
    new_version_num = max_version + 1

    restored_version = NoteVersion(
        note_id=note.id,
        version=new_version_num,
        content=note.content,
        editor_id=current_user.id,
    )

    db.add(note)
    db.add(restored_version)
    db.commit()
    db.refresh(restored_version)
    return restored_version
