from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .test_campaigns import get_gm_access_token
from app import crud, schemas

# @trace TASK-014


def test_create_tick_unauthorized(test_client: TestClient):
    """
    Test creating a tick without an access token fails with 401.
    """
    response = test_client.post(
        "/ticks",
        json={"campaign_id": 1, "narrative": "The beginning of the end."},
    )
    assert response.status_code == 401


def test_create_tick_for_nonexistent_campaign(test_client: TestClient):
    """
    Test creating a tick for a campaign that does not exist fails with 404.
    """
    token = get_gm_access_token(test_client, username="no_campaign_gm")
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.post(
        "/ticks",
        json={"campaign_id": 999, "narrative": "A tick for a ghost campaign."},
        headers=headers,
    )
    assert response.status_code == 404


def test_create_first_tick_success(test_client: TestClient):
    """
    Test successfully creating the first tick for a campaign.
    """
    # 1. Create a user and campaign
    token = get_gm_access_token(test_client, username="first_tick_gm")
    headers = {"Authorization": f"Bearer {token}"}
    campaign_data = {
        "name": "Campaign for Ticks",
        "description": "A campaign to test ticks.",
        "party_size": 4,
        "party_level": 1,
    }
    response = test_client.post("/campaigns", json=campaign_data, headers=headers)
    assert response.status_code == 201
    campaign = response.json()
    campaign_id = campaign["id"]

    # 2. Create the first tick
    tick_data = {"campaign_id": campaign_id, "narrative": "The very first tick."}
    response = test_client.post("/ticks", json=tick_data, headers=headers)

    # 3. Assertions
    assert response.status_code == 201
    data = response.json()
    assert data["campaign_id"] == campaign_id
    assert data["tick_number"] == 1
    assert data["narrative"] == "The very first tick."
    assert "id" in data


def test_create_second_tick_with_state_cascade(
    test_client: TestClient, db_session: Session
):
    """
    Test that creating a second tick cascades the assets from the first tick.
    """
    # 1. Create a user and campaign
    token = get_gm_access_token(test_client, username="cascade_gm")
    headers = {"Authorization": f"Bearer {token}"}
    campaign_data = {"name": "Cascade Campaign", "party_size": 4, "party_level": 1}
    res = test_client.post("/campaigns", json=campaign_data, headers=headers)
    assert res.status_code == 201
    campaign_id = res.json()["id"]

    # 2. Create the first tick
    first_tick_data = {"campaign_id": campaign_id, "narrative": "First tick"}
    res = test_client.post("/ticks", json=first_tick_data, headers=headers)
    assert res.status_code == 201
    first_tick_id = res.json()["id"]

    # 3. Create an asset in the first tick directly via CRUD
    asset_data = schemas.AssetCreate(
        tick_id=first_tick_id,
        asset_type="NPC",
        name="Gorok the Barbarian",
        description="A mighty warrior.",
        traits={"class": "Barbarian", "level": 5},
    )
    crud.create_asset(db=db_session, asset=asset_data)

    # 4. Create the second tick
    second_tick_data = {"campaign_id": campaign_id, "narrative": "Second tick"}
    res = test_client.post("/ticks", json=second_tick_data, headers=headers)
    assert res.status_code == 201
    second_tick_id = res.json()["id"]
    assert res.json()["tick_number"] == 2

    # 5. Verify the assets were cascaded to the second tick
    cascaded_assets = crud.get_assets_by_tick_id(db=db_session, tick_id=second_tick_id)
    assert len(cascaded_assets) == 1
    cascaded_asset = cascaded_assets[0]
    assert cascaded_asset.name == "Gorok the Barbarian"
    assert cascaded_asset.asset_type == "NPC"
    assert cascaded_asset.traits["level"] == 5
    assert cascaded_asset.tick_id == second_tick_id
