import os
import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_Kqo0hbYcQ7Et@ep-small-fog-a43n83zr-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"  # or a separate test DB URL

from app.main import app  # after env is set

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c
