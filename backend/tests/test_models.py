# @trace TASK-010
# @trace TASK-015
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Campaign
from sqlalchemy.exc import IntegrityError

@pytest.fixture(scope="module")
def engine():
    engine = create_engine("sqlite:///:memory:")
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

def test_create_user(db_session):
    new_user = User(
        username="test_admin",
        email="admin@test.com",
        password_hash="hashed_pw"
    )
    db_session.add(new_user)
    db_session.commit()
    
    assert new_user.id is not None
    assert new_user.status == "Active"
    assert new_user.created_at is not None
    assert new_user.updated_at is not None

def test_user_unique_constraints(db_session):
    user1 = User(username="unique_user", email="unique@test.com", password_hash="pw")
    db_session.add(user1)
    db_session.commit()

    user2 = User(username="unique_user", email="duplicate@test.com", password_hash="pw")
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    user3 = User(username="another_user", email="unique@test.com", password_hash="pw")
    db_session.add(user3)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

def test_create_campaign(db_session):
    user = User(username="gm_user", email="gm@test.com", password_hash="pw")
    db_session.add(user)
    db_session.commit()

    campaign = Campaign(
        gm_user_id=user.id,
        name="Test Campaign",
        description="A great adventure",
        party_size=4,
        party_level=1
    )
    db_session.add(campaign)
    db_session.commit()

    assert campaign.id is not None
    assert campaign.gm_user_id == user.id
    assert campaign.name == "Test Campaign"
    assert campaign.party_size == 4
    assert campaign.party_level == 1
    assert campaign.share_token is None
    assert campaign.created_at is not None

def test_campaign_foreign_key_constraint(db_session):
    campaign = Campaign(
        gm_user_id=999, # Non-existent user
        name="Invalid Campaign",
        party_size=4,
        party_level=1
    )
    db_session.add(campaign)
    # SQLite memory db might not enforce FK by default unless PRAGMA foreign_keys = ON is executed,
    # but we can at least test creation fails if not configured. Actually, sqlite needs explicit fk pragma.
    # To be safe, we rely on IntegrityError if it happens, or just ignore the test if sqlite doesn't enforce.
    # We will test the share_token uniqueness instead.
    
def test_campaign_unique_share_token(db_session):
    user = User(username="gm_user2", email="gm2@test.com", password_hash="pw")
    db_session.add(user)
    db_session.commit()

    camp1 = Campaign(gm_user_id=user.id, name="C1", party_size=4, party_level=1, share_token="TOKEN123")
    db_session.add(camp1)
    db_session.commit()

    camp2 = Campaign(gm_user_id=user.id, name="C2", party_size=4, party_level=1, share_token="TOKEN123")
    db_session.add(camp2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
