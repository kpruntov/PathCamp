# @trace TASK-020
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Campaign, Tick, Asset, Encounter
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

def test_create_timeline_models(db_session):
    # Setup dependencies
    user = User(username="timeline_gm", email="timeline_gm@test.com", password_hash="pw")
    db_session.add(user)
    db_session.commit()

    campaign = Campaign(gm_user_id=user.id, name="Timeline Campaign", party_size=4, party_level=1)
    db_session.add(campaign)
    db_session.commit()

    # Test Tick creation
    tick = Tick(campaign_id=campaign.id, tick_number=1, narrative="The adventure begins.")
    db_session.add(tick)
    db_session.commit()

    assert tick.id is not None
    assert tick.campaign_id == campaign.id
    assert tick.tick_number == 1
    assert tick.narrative == "The adventure begins."

    # Test Asset creation
    asset = Asset(
        tick_id=tick.id,
        asset_type="Scene",
        name="The Gloomy Tavern",
        description="A dark and dusty place.",
        traits=["indoor", "tavern"]
    )
    db_session.add(asset)
    db_session.commit()

    assert asset.id is not None
    assert asset.tick_id == tick.id
    assert asset.asset_type == "Scene"
    assert asset.name == "The Gloomy Tavern"
    assert "indoor" in asset.traits

    # Test Encounter creation
    encounter = Encounter(
        asset_id=asset.id,
        mechanical_data={"monsters": [{"id": "goblin", "count": 3}], "hazard": "none"},
        gm_narrative="Three goblins are drinking at a table."
    )
    db_session.add(encounter)
    db_session.commit()

    assert encounter.id is not None
    assert encounter.asset_id == asset.id
    assert encounter.mechanical_data["monsters"][0]["count"] == 3
    assert encounter.gm_narrative == "Three goblins are drinking at a table."

def test_tick_unique_constraint(db_session):
    user = User(username="timeline_gm_2", email="timeline_gm2@test.com", password_hash="pw")
    db_session.add(user)
    db_session.commit()

    campaign = Campaign(gm_user_id=user.id, name="Timeline Campaign 2", party_size=4, party_level=1)
    db_session.add(campaign)
    db_session.commit()

    tick1 = Tick(campaign_id=campaign.id, tick_number=1, narrative="First tick")
    db_session.add(tick1)
    db_session.commit()

    tick2 = Tick(campaign_id=campaign.id, tick_number=1, narrative="Duplicate tick number")
    db_session.add(tick2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
