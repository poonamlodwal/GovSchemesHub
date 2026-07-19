import json


def get_auth_token(client, email="creator@example.com"):
    client.post(
        "/api/auth/register",
        data=json.dumps({"name": "Creator", "email": email, "password": "secret123"}),
        content_type="application/json",
    )
    response = client.post(
        "/api/auth/login",
        data=json.dumps({"email": email, "password": "secret123"}),
        content_type="application/json",
    )
    return response.get_json()["data"]["access_token"]


def create_scheme(client, token, title="Farmer Subsidy Scheme"):
    return client.post(
        "/api/schemes",
        data=json.dumps(
            {
                "title": title,
                "description": "A subsidy scheme for farmers.",
                "category": "Agriculture",
                "eligibility": "Farmers owning less than 5 acres.",
                "benefits": "Up to 50000 INR subsidy.",
                "state": "Haryana",
            }
        ),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"},
    )


def test_create_scheme_requires_auth(client):
    response = client.post(
        "/api/schemes",
        data=json.dumps({"title": "X", "description": "Y", "category": "Z"}),
        content_type="application/json",
    )
    assert response.status_code == 401


def test_create_scheme_success(client):
    token = get_auth_token(client)
    response = create_scheme(client, token)
    body = response.get_json()
    assert response.status_code == 201
    assert body["data"]["scheme"]["title"] == "Farmer Subsidy Scheme"


def test_list_schemes(client):
    token = get_auth_token(client)
    create_scheme(client, token)
    response = client.get("/api/schemes")
    body = response.get_json()
    assert response.status_code == 200
    assert len(body["data"]) == 1


def test_get_single_scheme(client):
    token = get_auth_token(client)
    create_response = create_scheme(client, token)
    scheme_id = create_response.get_json()["data"]["scheme"]["id"]

    response = client.get(f"/api/schemes/{scheme_id}")
    body = response.get_json()
    assert response.status_code == 200
    assert body["data"]["scheme"]["id"] == scheme_id


def test_update_scheme_success(client):
    token = get_auth_token(client)
    create_response = create_scheme(client, token)
    scheme_id = create_response.get_json()["data"]["scheme"]["id"]

    response = client.put(
        f"/api/schemes/{scheme_id}",
        data=json.dumps({"title": "Updated Title"}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"},
    )
    body = response.get_json()
    assert response.status_code == 200
    assert body["data"]["scheme"]["title"] == "Updated Title"


def test_delete_scheme_success(client):
    token = get_auth_token(client)
    create_response = create_scheme(client, token)
    scheme_id = create_response.get_json()["data"]["scheme"]["id"]

    response = client.delete(
        f"/api/schemes/{scheme_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    get_response = client.get(f"/api/schemes/{scheme_id}")
    assert get_response.status_code == 404


def test_update_scheme_forbidden_for_other_user(client):
    token_a = get_auth_token(client, email="a@example.com")
    token_b = get_auth_token(client, email="b@example.com")

    create_response = create_scheme(client, token_a)
    scheme_id = create_response.get_json()["data"]["scheme"]["id"]

    response = client.put(
        f"/api/schemes/{scheme_id}",
        data=json.dumps({"title": "Hacked Title"}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert response.status_code == 403
