from fastapi import FastAPI
from app.api.v1 import auth, notes, versions
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Notes API with Version History")
origins=["http://127.0.0.1:5173",
    "http://localhost:5173",]

# @app.on_event("startup")
# def log_db_url():
#     print("### DATABASE_URL IN APP:",)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


app.include_router(auth.router, prefix="/api/v1")
app.include_router(notes.router, prefix="/api/v1")
app.include_router(versions.router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)