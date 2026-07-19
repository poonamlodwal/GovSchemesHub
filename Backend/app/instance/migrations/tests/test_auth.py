import json


def register_user(client, name="John Doe", email="john@example.com", password="secret123"):
    return client.post(
        "/api/auth/register",
        data=json.dumps({"name": name, "email": email, "password": password}),
        content_type="application/json",
    )


def login_user(client, email="john@example.com", password="secret123"):
    return client.post(
        "/api/auth/login",
        data=json.dumps({"email": email, "password": password}),
        content_type="application/json",
    )


def test_register_success(client):
    response = register_user(client)
    body = response.get_json()
    assert response.status_code == 201
    assert body["success"] is True
    assert body["data"]["user"]["email"] == "john@example.com"
    assert "access_token" in body["data"]


def test_register_duplicate_email(client):
    register_user(client)
    response = register_user(client)
    body = response.get_json()
    assert response.status_code == 409
    assert body["success"] is False


def test_register_validation_error(client):
    response = client.post(
        "/api/auth/register",
        data=json.dumps({"name": "", "email": "bad-email", "password": "123"}),
        content_type="application/json",
    )
    body = response.get_json()
    assert response.status_code == 422
    assert "errors" in body


def test_login_success(client):
    register_user(client)
    response = login_user(client)
    body = response.get_json()
    assert response.status_code == 200
    assert body["success"] is True
    assert "access_token" in body["data"]


def test_login_invalid_credentials(client):
    register_user(client)
    response = login_user(client, password="wrongpassword")
    body = response.get_json()
    assert response.status_code == 401
    assert body["success"] is False


def test_profile_requires_auth(client):
    response = client.get("/api/auth/profile")
    assert response.status_code == 401


def test_profile_with_token(client):
    register_user(client)
    login_response = login_user(client)
    token = login_response.get_json()["data"]["access_token"]

    response = client.get(
        "/api/auth/profile", headers={"Authorization": f"Bearer {token}"}
    )
    body = response.get_json()
    assert response.status_code == 200
    assert body["data"]["user"]["email"] == "john@example.com"
