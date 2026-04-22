from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import crud

# @trace TASK-012


def get_gm_access_token(test_client: TestClient, username: str = "test_gm") -> str:
    """
    Helper function to create a user and get an access token for them.
    """
    # Create a user
    test_client.post(
        "/users/",
        json={
            "email": f"{username}@example.com",
            "username": username,
            "password": "password123",
        },
    )
    # Login to get a token
    response = test_client.post(
        "/login",
        json={"username": username, "password": "password123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_create_campaign_unauthorized(test_client: TestClient):
    """
    Test creating a campaign without an access token fails with 401.
    """
    campaign_data = {
        "name": "My First Campaign",
        "description": "A test campaign.",
        "party_size": 4,
        "party_level": 1,
    }
    response = test_client.post("/campaigns", json=campaign_data)
    assert response.status_code == 401


def test_create_campaign_success(test_client: TestClient):
    """
    Test successful creation of a new campaign.
    """
    token = get_gm_access_token(test_client)
    headers = {"Authorization": f"Bearer {token}"}
    campaign_data = {
        "name": "The Lost Mines",
        "description": "A classic adventure.",
        "party_size": 5,
        "party_level": 1,
    }

    response = test_client.post("/campaigns", json=campaign_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "The Lost Mines"
    assert data["description"] == "A classic adventure."
    assert data["party_size"] == 5
    assert data["party_level"] == 1
    assert "id" in data
    assert "gm_user_id" in data


def test_create_campaign_duplicate_name(test_client: TestClient):
    """
    Test that creating a campaign with a duplicate name for the same user fails.
    """
    token = get_gm_access_token(test_client, username="duplicate_gm")
    headers = {"Authorization": f"Bearer {token}"}
    campaign_data = {
        "name": "The Duplicate Saga",
        "description": "First instance.",
        "party_size": 4,
        "party_level": 1,
    }

    # First creation should succeed
    response1 = test_client.post("/campaigns", json=campaign_data, headers=headers)
    assert response1.status_code == 201

    # Second creation with the same name should fail
    response2 = test_client.post("/campaigns", json=campaign_data, headers=headers)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]


def test_create_campaign_missing_fields(test_client: TestClient):
    """
    Test that creating a campaign with missing required fields fails.
    """
    token = get_gm_access_token(test_client, username="missing_fields_gm")
    headers = {"Authorization": f"Bearer {token}"}

    # Missing 'name'
    campaign_data = {
        "description": "A test campaign.",
        "party_size": 4,
        "party_level": 1,
    }
    response = test_client.post("/campaigns", json=campaign_data, headers=headers)
    assert response.status_code == 422  # Unprocessable Entity


def test_generate_share_link_unauthorized(test_client: TestClient):
    """
    Test that generating a share link without authentication fails with 401.
    """
    response = test_client.get("/campaigns/1/share")
    assert response.status_code == 401


def test_generate_share_link_success(test_client: TestClient, db_session: Session):
    """
    Test that generating a share link with authentication succeeds and saves the token.
    """
    # 1. Create user and campaign
    token = get_gm_access_token(test_client, username="share_gm")
    headers = {"Authorization": f"Bearer {token}"}
    campaign_data = {"name": "Sharable Campaign", "party_size": 4, "party_level": 1}
    res = test_client.post("/campaigns", json=campaign_data, headers=headers)
    assert res.status_code == 201
    campaign_id = res.json()["id"]

    # 2. Generate share link
    response = test_client.get(f"/campaigns/{campaign_id}/share", headers=headers)

    # 3. Assertions
    assert response.status_code == 200
    data = response.json()
    assert "share_url" in data
    
    # 4. Verify token in DB
    share_token = data["share_url"].split("/")[-1]
    db_campaign = crud.get_campaign_by_share_token(db=db_session, token=share_token)
    assert db_campaign is not None
    assert db_campaign.id == campaign_id


def test_get_shared_campaign_success(test_client: TestClient):
    """
    Test that a shared campaign can be accessed via its share token.
    """
    # 1. Create user and campaign, and generate share link
    token = get_gm_access_token(test_client, username="shared_campaign_gm")
    headers = {"Authorization": f"Bearer {token}"}
    campaign_data = {"name": "A Shared Story", "description": "Public view.", "party_size": 3, "party_level": 2}
    res = test_client.post("/campaigns", json=campaign_data, headers=headers)
    assert res.status_code == 201
    campaign_id = res.json()["id"]
    res = test_client.get(f"/campaigns/{campaign_id}/share", headers=headers)
    assert res.status_code == 200
    share_token = res.json()["share_url"].split("/")[-1]

    # 2. Access the shared campaign without auth
    response = test_client.get(f"/shared/{share_token}")

    # 3. Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "A Shared Story"
    assert data["id"] == campaign_id
    assert "gm_user_id" not in data # Ensure sensitive data is not exposed


def test_get_shared_campaign_not_found(test_client: TestClient):
    """
    Test that accessing a shared campaign with an invalid token fails.
    """
    response = test_client.get("/shared/invalid-token")
    assert response.status_code == 404


# @trace TASK-013
