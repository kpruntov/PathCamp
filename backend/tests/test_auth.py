def test_create_user(test_client):
    """
    Test creating a new user.
    """
    response = test_client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123",
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data
    assert "password_hash" not in data  # Ensure password hash is not returned


def test_login_for_access_token(test_client):
    """
    Test logging in to get an access token.
    """
    # First, create a user to test login
    test_client.post(
        "/users/",
        json={
            "email": "loginuser@example.com",
            "username": "loginuser",
            "password": "password123",
        },
    )

    response = test_client.post(
        "/login",
        json={"username": "loginuser", "password": "password123"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_for_access_token_wrong_password(test_client):
    """
    Test logging in with the wrong password.
    """
    # First, create a user to test login
    test_client.post(
        "/users/",
        json={
            "email": "wrongpass@example.com",
            "username": "wrongpass",
            "password": "password123",
        },
    )

    response = test_client.post(
        "/login",
        json={"username": "wrongpass", "password": "wrongpassword"},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Incorrect username or password"


def test_login_for_access_token_wrong_username(test_client):
    """
    Test logging in with the wrong username.
    """
    response = test_client.post(
        "/login",
        json={"username": "nonexistentuser", "password": "password123"},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Incorrect username or password"


def test_logout(test_client):
    """
    Test logging out. This is a placeholder for now as proper token invalidation is not implemented.
    It just checks that the endpoint exists and returns a success status.
    """
    response = test_client.post("/logout")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Logout successful"}


# @trace TASK-007
# @trace TASK-008
