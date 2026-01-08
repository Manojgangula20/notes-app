def test_register_and_login(client):
    # register
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "test2@example.com", "password": "secret123"},
    )
    assert resp.status_code in (201, 400)
    # if 400, it’s "Email already registered"

    # login
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "test2@example.com", "password": "secret123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
