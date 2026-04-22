from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import crud, schemas
from .test_campaigns import get_gm_access_token

# @trace TASK-010

def test_get_users_unauthorized(test_client: TestClient):
    """
    Test that getting users without authentication fails with 401.
    """
    response = test_client.get("/admin/users")
    assert response.status_code == 401


def test_get_users_as_non_admin(test_client: TestClient):
    """
    Test that getting users as a non-admin user fails with 403.
    """
    token = get_gm_access_token(test_client, username="non_admin_user")
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get("/admin/users", headers=headers)
    assert response.status_code == 403


def test_get_users_as_admin(test_client: TestClient, db_session: Session):
    """
    Test that getting users as an admin user succeeds.
    """
    # 1. Create a user and then promote them to Admin
    admin_username = "admin_user"
    admin_password = "password123"
    test_client.post(
        "/users/",
        json={
            "email": f"{admin_username}@example.com",
            "username": admin_username,
            "password": admin_password,
        },
    )
    admin_user = crud.get_user_by_username(db=db_session, username=admin_username)
    assert admin_user is not None
    admin_user.role = "Admin"
    db_session.commit()
    db_session.refresh(admin_user)

    # 2. Log in as the new admin to get a token with the correct role
    response = test_client.post(
        "/login",
        json={"username": admin_username, "password": admin_password},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Call the endpoint
    response = test_client.get("/admin/users", headers=headers)

    # 4. Assertions
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(user["username"] == admin_username for user in data)
