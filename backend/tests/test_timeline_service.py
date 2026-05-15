# @trace TASK-021
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Campaign, Tick, Asset, Encounter
from app.services import timeline
from app import schemas
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

def test_initialize_timeline(db_session):
    user = User(username="tl_admin", email="tl@test.com", password_hash="pw")
    db_session.add(user)
    db_session.commit()
    campaign = Campaign(gm_user_id=user.id, name="TL Camp", party_size=4, party_level=1)
    db_session.add(campaign)
    db_session.commit()

    tick = timeline.initialize_timeline(db_session, campaign.id)
    assert tick is not None
    assert tick.tick_number == 1
    assert tick.narrative == "Campaign started."

def test_create_next_tick_cascades_assets(db_session):
    user = User(username="tl_admin2", email="tl2@test.com", password_hash="pw")
    db_session.add(user)
    db_session.commit()
    campaign = Campaign(gm_user_id=user.id, name="TL Camp2", party_size=4, party_level=1)
    db_session.add(campaign)
    db_session.commit()
    
    first_tick = timeline.initialize_timeline(db_session, campaign.id)
    
    asset_data = schemas.AssetCreate(
        asset_type="NPC",
        name="Bob",
        description="A friendly barkeep",
        traits=["human"]
    )
    asset = timeline.create_asset_in_tick(db_session, first_tick.id, asset_data)
    
    # Create next tick
    new_tick_id = timeline.create_next_tick(db_session, campaign.id, "The party sleeps.")
    assert new_tick_id is not None
    
    new_tick = db_session.query(Tick).filter_by(id=new_tick_id).first()
    assert new_tick.tick_number == 2
    assert new_tick.narrative == "The party sleeps."
    
    # Check if asset cascaded
    assets_in_new_tick = db_session.query(Asset).filter_by(tick_id=new_tick_id).all()
    assert len(assets_in_new_tick) == 1
    assert assets_in_new_tick[0].name == "Bob"

def test_update_tick(db_session):
    user = User(username="tl_admin3", email="tl3@test.com", password_hash="pw")
    db_session.add(user)
    db_session.commit()
    campaign = Campaign(gm_user_id=user.id, name="TL Camp3", party_size=4, party_level=1)
    db_session.add(campaign)
    db_session.commit()
    
    tick = timeline.initialize_timeline(db_session, campaign.id)
    success = timeline.update_tick(db_session, tick.id, "Updated narrative")
    assert success is True
    
    updated_tick = db_session.query(Tick).filter_by(id=tick.id).first()
    assert updated_tick.narrative == "Updated narrative"

def test_create_and_update_asset(db_session):
    user = User(username="tl_admin4", email="tl4@test.com", password_hash="pw")
    db_session.add(user)
    db_session.commit()
    campaign = Campaign(gm_user_id=user.id, name="TL Camp4", party_size=4, party_level=1)
    db_session.add(campaign)
    db_session.commit()
    
    tick = timeline.initialize_timeline(db_session, campaign.id)
    asset_data = schemas.AssetCreate(
        asset_type="Item",
        name="Sword",
        traits=["metal"]
    )
    asset = timeline.create_asset_in_tick(db_session, tick.id, asset_data)
    assert asset is not None
    
    update_data = schemas.AssetCreate(
        asset_type="Item",
        name="Sword +1",
        traits=["metal", "magic"]
    )
    success = timeline.update_asset_in_tick(db_session, asset.id, update_data)
    assert success is True
    
    updated_asset = db_session.query(Asset).filter_by(id=asset.id).first()
    assert updated_asset.name == "Sword +1"

def test_save_encounter_to_tick(db_session):
    user = User(username="tl_admin5", email="tl5@test.com", password_hash="pw")
    db_session.add(user)
    db_session.commit()
    campaign = Campaign(gm_user_id=user.id, name="TL Camp5", party_size=4, party_level=1)
    db_session.add(campaign)
    db_session.commit()
    
    tick = timeline.initialize_timeline(db_session, campaign.id)
    asset_data = schemas.AssetCreate(asset_type="Scene", name="Forest")
    asset = timeline.create_asset_in_tick(db_session, tick.id, asset_data)
    
    encounter_data = schemas.EncounterCreate(
        mechanical_data={"monsters": []},
        gm_narrative="Quiet forest"
    )
    success = timeline.save_encounter_to_tick(db_session, asset.id, encounter_data)
    assert success is True
    
    encounter = db_session.query(Encounter).filter_by(asset_id=asset.id).first()
    assert encounter is not None
    assert encounter.gm_narrative == "Quiet forest"

def test_get_timeline(db_session):
    user = User(username="tl_admin6", email="tl6@test.com", password_hash="pw")
    db_session.add(user)
    db_session.commit()
    campaign = Campaign(gm_user_id=user.id, name="TL Camp6", party_size=4, party_level=1)
    db_session.add(campaign)
    db_session.commit()
    
    timeline.initialize_timeline(db_session, campaign.id)
    timeline_data = timeline.get_timeline(db_session, campaign.id)
    
    assert timeline_data is not None
    assert len(timeline_data.ticks) == 1
