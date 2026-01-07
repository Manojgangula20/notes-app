from datetime import datetime

from pydantic import BaseModel


class VersionOut(BaseModel):
    id: int
    note_id: int
    version: int
    content: str
    editor_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True
