from fastapi import APIRouter

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/ping")
def notes_ping():
    return {"message": "notes ok"}
