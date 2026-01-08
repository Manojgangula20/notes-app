# Notes API with Version History

FastAPI **backend** for a note‑taking application with PostgreSQL, JWT authentication, and full note version history (create, update, restore previous versions), plus a simple React frontend and Postman [text](notes-frontend)documentation. 

## Features

- User registration and login with JWT bearer tokens.  
- Secure password hashing (no plain‑text passwords).   
- CRUD operations for notes (create, list, get, update, delete) per authenticated user.   
- Automatic **version history**: every note update stores a new version with timestamp and editor. 
- Endpoints to list all versions, fetch a specific version, and restore a previous version.  
- Pytest test suite for core flows (auth, notes, version history). 
- Postman collection with examples and tests.  
- Simple React frontend (Vite) integrating auth + notes. 
## Tech stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic, Alembic.   
- **Database**: PostgreSQL hosted on Neon (or any Postgres).  
- **Auth**: JWT (OAuth2 password flow with bearer tokens).   
- **Frontend**: React + Vite (simple single‑page UI).   
- **Tests**: pytest. 
- **Docs & Tools**: Postman collection. 

## Project structure

```text
.
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py        # /api/v1/auth/register, /api/v1/auth/login
│   │   │   ├── notes.py       # /api/v1/notes CRUD
│   │   │   └── versions.py    # /api/v1/notes/{id}/versions
│   │   └── deps.py            # DB/session dependencies
│   ├── core/
│   │   ├── config.py          # settings & env vars
│   │   └── security.py        # hashing, JWT helpers
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   └── main.py                # FastAPI app, CORS, router includes
├── alembic/                   # migrations
├── notes-frontend/            # React/Vite frontend
├── tests/                     # pytest tests
├── postman/
│   └── Notes-API.postman_collection.json
└── README.md
```
## Environment variables

Backend uses environment variables via `app/core/config.py`. 

Create a `.env` in the project root:

```env
DATABASE_URL=postgresql+psycopg2://user:password@host:port/dbname
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60
ENVIRONMENT=development

DATABASE_URL: your Neon (or other Postgres) connection string. 

SECRET_KEY: any strong random string for signing JWTs. 

ACCESS_TOKEN_EXPIRE_MINUTES: token lifetime in minutes. 
```
## Backend setup (local)
## Install dependencies

```bash

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

```
## Run migrations
```bash
alembic upgrade head
```
## Start the API
```bash
uvicorn app.main:app --reload
```
* Local base URL: http://127.0.0.1:8000

* Interactive docs: http://127.0.0.1:8000/docs 

## Frontend setup (local)
## From repo root: 

```bash
cd notes-frontend
npm install
npm run dev
```
* Vite dev server: usually http://127.0.0.1:5173 

## Frontend configuration
## ```notes-frontend/src/App.jsx``` contains the API base URL:

```js
const API_BASE = "http://127.0.0.1:8000/api/v1";
```
For local dev, ensure this matches how routers are mounted in main.py. 


API overview
Base URL pattern:

Local: http://127.0.0.1:8000/api/v1

Deployed: https://<your-backend-host>/api/v1 

Auth
POST /api/v1/auth/register
Body (JSON):

```json
{
  "email": "user@example.com",
  "password": "string"
}
```
Response: created user (without password). 

POST ```/api/v1/auth/login```
Body: ```application/x-www-form-urlencoded```:

```username```: email

```password```: password

Response:

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```
Use ```Authorization: Bearer <token>``` for all protected endpoints.

## Notes
GET ```/api/v1/notes``` – list all notes for current user. [file:1]

POST ```/api/v1/notes``` – create a note.

```json
{
  "title": "Sample note",
  "content": "Hello"
}
```
GET ```/api/v1/notes/{note_id}``` – get single note.

PUT ```/api/v1/notes/{note_id}``` – update title/content.

DELETE ```/api/v1/notes/{note_id}``` – delete note.

Each note includes `id`, `title`, `content`, `owner_id`, `created_at`, `updated_at`. 

## Version history
GET `/api/v1/notes/{note_id}/versions` – list all versions for a note.

GET `/api/v1/notes/{note_id}/versions/{version}` – get a specific version.

POST `/api/v1/notes/{note_id}/versions/{version}/restore` – restore note to that version.

Every update automatically creates a new version with version number, snapshot content, editor, and timestamp.

## Postman collection
A Postman collection is provided at:

```text
postman/Notes-API.postman_collection.json
```
The collection includes:

Auth: register, login (and token variable storage). 

Notes: create, list, get, update, delete. 

Versions: list, get, restore. 

Usage:

1. Import the collection into Postman.

2. Set the base_url variable to your backend URL (local or deployed).

3. Run Auth / Login first to populate token.

4. Use notes and versions requests; tests validate status codes and key fields. 

## Running tests
From repo root:

```bash
pytest

```
Tests cover:

1. User registration and login.

2. Access to protected endpoints.

3. CRUD operations on notes.

4. Version history creation and retrieval. 

## Deployment
The backend can be deployed to services like Render, Railway, Fly.io, or Azure App Service. 

## Typical steps:

1. Set `DATABASE_URL`, `SECRET_KEY` and `ACCESS_TOKEN_EXPIRE_MINUTES` as environment variables on the platform.

2. Run Alembic migrations (`alembic upgrade head`) via a deploy or release command. 

3. Start app with:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
4. Update:

  * Postman base_url to the deployed URL.

  * Frontend API_BASE to the deployed /api/v1 base. 



Notes on API versioning
All endpoints are mounted under /api/v1/... to support future versions (e.g. /api/v2/...) without breaking existing clients. 
