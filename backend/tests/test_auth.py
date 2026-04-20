from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    """
    Test creating a new user.
    """
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "username": "testuser", "password": "password123"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data
    assert "password_hash" not in data # Ensure password hash is not returned

# @trace TASK-007
