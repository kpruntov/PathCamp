# @trace TASK-022
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

@pytest.fixture
def auth_headers(client):
    # Register and login to get token
    client.post("/auth/register", json={"username": "tl_api_gm", "email": "tl_api@test.com", "password": "pw"})
    response = client.post("/auth/login", json={"username": "tl_api_gm", "password": "pw"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def campaign(client, auth_headers):
    response = client.post("/campaigns", json={"name": "API Camp", "party_size": 4, "party_level": 1}, headers=auth_headers)
    return response.json()

def test_timeline_flow(client, auth_headers, campaign):
    campaign_id = campaign["id"]

    # 1. Timeline is empty initially (or creates a first tick, but wait, we need to init it or the first tick is created manually?)
    # According to our service, timeline initialize_timeline is not exposed via API, 
    # but create_next_tick will create tick 1 if it doesn't exist.

    # 2. Create Next Tick
    resp = client.post("/ticks", json={"campaign_id": campaign_id, "narrative": "A new beginning"}, headers=auth_headers)
    assert resp.status_code == 201
    tick_id = resp.json()["new_tick_id"]
    assert tick_id > 0

    # 3. Update Tick
    resp = client.put(f"/ticks/{tick_id}", json={"narrative": "A modified beginning"}, headers=auth_headers)
    assert resp.status_code == 200

    # 4. Create Asset
    asset_data = {
        "asset_type": "NPC",
        "name": "Goblin King",
        "description": "A fierce leader",
        "traits": ["goblin", "boss"]
    }
    resp = client.post(f"/ticks/{tick_id}/assets", json=asset_data, headers=auth_headers)
    assert resp.status_code == 201
    asset_id = resp.json()["asset_id"]
    assert asset_id > 0

    # 5. Create Encounter
    encounter_data = {
        "mechanical_data": {"enemies": ["Goblin King"]},
        "gm_narrative": "He attacks!"
    }
    resp = client.post(f"/ticks/{tick_id}/scenes/{asset_id}/encounter", json=encounter_data, headers=auth_headers)
    assert resp.status_code == 200

    # 6. Get Timeline
    resp = client.get(f"/campaigns/{campaign_id}/timeline", headers=auth_headers)
    assert resp.status_code == 200
    timeline = resp.json()
    assert timeline["campaign_id"] == campaign_id
    assert len(timeline["ticks"]) == 2
    assert timeline["ticks"][1]["narrative"] == "A modified beginning"
    assert len(timeline["ticks"][1]["assets"]) == 1
    assert timeline["ticks"][1]["assets"][0]["name"] == "Goblin King"

def test_timeline_authorization(client, auth_headers, campaign):
    campaign_id = campaign["id"]

    # Register a second user to test unauthorized access
    client.post("/auth/register", json={"username": "other_gm", "email": "other@test.com", "password": "pw"})
    response = client.post("/auth/login", json={"username": "other_gm", "password": "pw"})
    token2 = response.json()["access_token"]
    auth_headers2 = {"Authorization": f"Bearer {token2}"}

    # 1. Other user tries to create a tick
    resp = client.post("/ticks", json={"campaign_id": campaign_id, "narrative": "Hacked tick"}, headers=auth_headers2)
    assert resp.status_code == 403

    # Need a valid tick to test update/delete
    resp = client.post("/ticks", json={"campaign_id": campaign_id, "narrative": "Valid tick"}, headers=auth_headers)
    assert resp.status_code == 201
    tick_id = resp.json()["new_tick_id"]

    # 2. Other user tries to update tick
    resp = client.put(f"/ticks/{tick_id}", json={"narrative": "Hacked update"}, headers=auth_headers2)
    assert resp.status_code == 403

    # 3. Other user tries to add asset
    asset_data = {
        "asset_type": "NPC",
        "name": "Hacked Asset",
        "description": "A fierce leader",
        "traits": []
    }
    resp = client.post(f"/ticks/{tick_id}/assets", json=asset_data, headers=auth_headers2)
    assert resp.status_code == 403
