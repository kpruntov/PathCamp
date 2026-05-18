# @trace TASK-017
# @trace TASK-042
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base
from app.main import app
from app.models import User, Campaign
import uuid

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
def test_user(db_session):
    unique_suffix = str(uuid.uuid4())[:8]
    user = User(username=f"testgm_{unique_suffix}", email=f"gm_{unique_suffix}@test.com", password_hash="pw", role="GM")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def test_get_campaigns(client, db_session, test_user):
    from app.dependencies import get_current_active_user
    app.dependency_overrides[get_current_active_user] = lambda: test_user
    
    # Create two campaigns for test_user
    c1 = Campaign(gm_user_id=test_user.id, name="Campaign 1", party_size=4, party_level=1)
    c2 = Campaign(gm_user_id=test_user.id, name="Campaign 2", party_size=5, party_level=2)
    db_session.add_all([c1, c2])
    db_session.commit()

    response = client.get("/campaigns")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Campaign 1"
    assert data[1]["name"] == "Campaign 2"

    app.dependency_overrides.pop(get_current_active_user, None)

def test_get_all_campaigns(client, db_session, test_user):
    c1 = Campaign(gm_user_id=test_user.id, name="Global Campaign 1", party_size=4, party_level=1)
    db_session.add(c1)
    db_session.commit()
    
    # Unauthenticated request
    response = client.get("/campaigns/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    names = [c["name"] for c in data]
    assert "Global Campaign 1" in names

def test_create_campaign(client, test_user):
    from app.dependencies import get_current_active_user
    app.dependency_overrides[get_current_active_user] = lambda: test_user

    response = client.post(
        "/campaigns",
        json={"name": "New Campaign", "description": "Epic", "party_size": 4, "party_level": 1}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Campaign"
    assert "id" in data
    
    app.dependency_overrides.pop(get_current_active_user, None)

def test_get_campaign_share_link(client, test_user):
    from app.dependencies import get_current_active_user
    app.dependency_overrides[get_current_active_user] = lambda: test_user

    # First create a campaign
    create_response = client.post(
        "/campaigns",
        json={"name": "Share Me", "party_size": 4, "party_level": 1}
    )
    campaign_id = create_response.json()["id"]

    # Now get the share link
    share_response = client.get(f"/campaigns/{campaign_id}/share")
    assert share_response.status_code == 200
    data = share_response.json()
    assert "share_url" in data
    assert "share/" in data["share_url"]

    app.dependency_overrides.pop(get_current_active_user, None)

def test_get_shared_campaign(client, db_session, test_user):
    # Directly insert a campaign with a share token into the DB
    token = str(uuid.uuid4())
    campaign = Campaign(gm_user_id=test_user.id, name="Shared Campaign", party_size=5, party_level=2, share_token=token)
    db_session.add(campaign)
    db_session.commit()
    db_session.refresh(campaign)

    # Access it via the share token (no auth required)
    response = client.get(f"/shared/{token}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Shared Campaign"
    assert data["party_size"] == 5

def test_get_shared_campaign_not_found(client):
    response = client.get("/shared/invalid-token")
    assert response.status_code == 404

def test_delete_campaign(client, db_session, test_user):
    from app.dependencies import get_current_active_user
    app.dependency_overrides[get_current_active_user] = lambda: test_user

    # Create a campaign
    create_response = client.post(
        "/campaigns",
        json={"name": "To Be Deleted", "party_size": 4, "party_level": 1}
    )
    campaign_id = create_response.json()["id"]

    # Delete the campaign
    delete_response = client.delete(f"/campaigns/{campaign_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"success": True}

    # Verify it's gone
    from app.models import Campaign
    assert db_session.query(Campaign).filter(Campaign.id == campaign_id).first() is None

    app.dependency_overrides.pop(get_current_active_user, None)

def test_delete_campaign_not_owner(client, db_session, test_user):
    from app.dependencies import get_current_active_user
    app.dependency_overrides[get_current_active_user] = lambda: test_user

    # Create a campaign owned by someone else
    other_user = User(username="other_gm", email="other@test.com", password_hash="pw", role="GM")
    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    other_campaign = Campaign(gm_user_id=other_user.id, name="Other Campaign", party_size=4, party_level=1)
    db_session.add(other_campaign)
    db_session.commit()
    db_session.refresh(other_campaign)

    # Attempt to delete
    delete_response = client.delete(f"/campaigns/{other_campaign.id}")
    assert delete_response.status_code == 404 # Or 403, typically 404 if filtering by user id
    
    app.dependency_overrides.pop(get_current_active_user, None)
