# @trace TASK-011
# @trace TASK-012
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base
from app.main import app

@pytest.fixture(scope="module")
def engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture(scope="function")
def client(db_session):
    from app.dependencies import get_db
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_register_user(client):
    response = client.post(
        "/register",
        json={"username": "testuser", "email": "test@test.com", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "user_id" in data
    assert data["message"] == "User registered successfully"

def test_login_user(client):
    client.post(
        "/register",
        json={"username": "testuser2", "email": "test2@test.com", "password": "password123"}
    )
    response = client.post(
        "/login",
        json={"username": "testuser2", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_logout_user(client):
    response = client.post("/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logout successful"

def test_get_user_list(client):
    client.post(
        "/register",
        json={"username": "testuser3", "email": "test3@test.com", "password": "password123"}
    )
    # Login to get token
    login_res = client.post(
        "/login",
        json={"username": "testuser3", "password": "password123"}
    )
    token = login_res.json()["access_token"]
    
    response = client.get(
        "/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert len(data["users"]) >= 1
    usernames = [u["username"] for u in data["users"]]
    assert "testuser3" in usernames

def test_update_user_status(client):
    reg_res = client.post(
        "/register",
        json={"username": "testuser4", "email": "test4@test.com", "password": "password123"}
    )
    user_id = reg_res.json()["user_id"]

    login_res = client.post(
        "/login",
        json={"username": "testuser4", "password": "password123"}
    )
    token = login_res.json()["access_token"]

    response = client.put(
        f"/admin/users/{user_id}/status",
        json={"status": "Inactive"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert str(data["user_id"]) == str(user_id)
    assert data["status"] == "Inactive"
