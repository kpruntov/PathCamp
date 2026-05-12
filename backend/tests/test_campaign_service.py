# @trace TASK-016
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.services import campaign as campaign_service
from app.schemas import CampaignCreate
from app.models import User, Campaign
import uuid

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_create_campaign(db_session, monkeypatch):
    # Mock the timeline service since it's not implemented yet
    monkeypatch.setattr("app.services.timeline.initialize_timeline", lambda db, cid: None)

    # Setup user
    user = User(username="gm1", email="gm1@test.com", password_hash="pw")
    db_session.add(user)
    db_session.commit()
    
    # Test Create
    campaign_in = CampaignCreate(name="My Campaign", description="Desc", party_size=4, party_level=1)
    campaign = campaign_service.create_campaign(db_session, user.id, campaign_in)
    
    assert campaign.id is not None
    assert campaign.name == "My Campaign"
    assert campaign.gm_user_id == user.id

def test_generate_share_link(db_session):
    # Setup user and campaign
    user = User(username="gm2", email="gm2@test.com", password_hash="pw")
    db_session.add(user)
    db_session.commit()
    campaign = Campaign(gm_user_id=user.id, name="C2", party_size=4, party_level=1)
    db_session.add(campaign)
    db_session.commit()
    
    # Test Share Link
    share_url = campaign_service.generate_share_link(db_session, campaign.id, base_url="http://localhost")
    assert "http://localhost/share/" in share_url
    
    # Verify token saved
    db_session.refresh(campaign)
    assert campaign.share_token is not None
    assert share_url.endswith(campaign.share_token)

def test_get_shared_campaign(db_session):
    # Setup user and campaign with token
    user = User(username="gm3", email="gm3@test.com", password_hash="pw")
    db_session.add(user)
    db_session.commit()
    token = str(uuid.uuid4())
    campaign = Campaign(gm_user_id=user.id, name="C3", party_size=4, party_level=1, share_token=token)
    db_session.add(campaign)
    db_session.commit()
    
    # Test Get
    shared_data = campaign_service.get_shared_campaign(db_session, token)
    assert shared_data is not None
    assert shared_data.name == "C3"
    assert shared_data.gm_user_id == user.id

def test_get_shared_campaign_not_found(db_session):
    # Test Get with invalid token
    shared_data = campaign_service.get_shared_campaign(db_session, "invalid_token")
    assert shared_data is None
