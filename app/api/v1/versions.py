from fastapi import APIRouter

router = APIRouter(prefix="/notes", tags=["versions"])


@router.get("/{note_id}/versions/ping")
def versions_ping(note_id: int):
    return {"message": f"versions ok for note {note_id}"}
