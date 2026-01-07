from fastapi import FastAPI
from app.api.v1 import auth, notes, versions

app = FastAPI(title="Notes API with Version History")


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


app.include_router(auth.router, prefix="/api/v1")
app.include_router(notes.router, prefix="/api/v1")
app.include_router(versions.router, prefix="/api/v1")
