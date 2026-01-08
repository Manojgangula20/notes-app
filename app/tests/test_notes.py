def get_token(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "notes@example.com", "password": "secret123"},
    )
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "notes@example.com", "password": "secret123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return resp.json()["access_token"]


def test_notes_crud_and_versions(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # create
    r = client.post(
        "/api/v1/notes",
        json={"title": "First", "content": "Hello"},
        headers=headers,
    )
    assert r.status_code == 201
    note = r.json()
    note_id = note["id"]

    # update
    r = client.put(
        f"/api/v1/notes/{note_id}",
        json={"content": "Hello v2"},
        headers=headers,
    )
    assert r.status_code == 200

    # list versions
    r = client.get(f"/api/v1/notes/{note_id}/versions", headers=headers)
    assert r.status_code == 200
    versions = r.json()
    assert len(versions) >= 2

    # restore version 1
    r = client.post(
        f"/api/v1/notes/{note_id}/versions/1/restore",
        headers=headers,
    )
    assert r.status_code == 200
