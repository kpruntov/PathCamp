from fastapi.testclient import TestClient

# @trace TASK-009


def get_access_token(test_client: TestClient) -> str:
    """
    Helper function to create a user and get an access token.
    """
    # Create a user
    test_client.post(
        "/users/",
        json={
            "email": "auth_test@example.com",
            "username": "auth_test_user",
            "password": "password123",
        },
    )
    # Login to get a token
    response = test_client.post(
        "/login",
        json={"username": "auth_test_user", "password": "password123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_access_protected_route_with_valid_token(test_client):
    """
    Tests that a protected route can be accessed with a valid token.
    """
    token = get_access_token(test_client)
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "auth_test_user"
    assert data["email"] == "auth_test@example.com"


def test_access_protected_route_without_token(test_client):
    """
    Tests that a protected route cannot be accessed without a token.
    """
    response = test_client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_access_protected_route_with_invalid_token(test_client):
    """
    Tests that a protected route cannot be accessed with an invalid token.
    """
    headers = {"Authorization": "Bearer an_invalid_token"}
    response = test_client.get("/users/me", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_access_protected_route_with_malformed_header(test_client):
    """
    Tests that a protected route returns an error with a malformed Authorization header.
    """
    token = get_access_token(test_client)
    headers = {"Authorization": f"Bear {token}"}  # Malformed "Bear" instead of "Bearer"
    response = test_client.get("/users/me", headers=headers)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
