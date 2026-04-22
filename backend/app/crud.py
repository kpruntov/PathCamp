from sqlalchemy.orm import Session
import secrets
from . import models, schemas
from .hashing import Hasher


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = Hasher.get_password_hash(user.password)
    db_user = models.User(
        email=user.email, username=user.username, password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_campaign_by_name(db: Session, name: str, gm_user_id: int):
    return (
        db.query(models.Campaign)
        .filter(models.Campaign.name == name, models.Campaign.gm_user_id == gm_user_id)
        .first()
    )


def get_campaign_by_id(db: Session, campaign_id: int, gm_user_id: int):
    return (
        db.query(models.Campaign)
        .filter(
            models.Campaign.id == campaign_id, models.Campaign.gm_user_id == gm_user_id
        )
        .first()
    )


def create_campaign(db: Session, campaign: schemas.CampaignCreate, gm_user_id: int):
    db_campaign = models.Campaign(**campaign.model_dump(), gm_user_id=gm_user_id)
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    # TODO: Initialize timeline with Tick 1 (FR-003)
    return db_campaign


def get_assets_by_tick_id(db: Session, tick_id: int):
    return db.query(models.Asset).filter(models.Asset.tick_id == tick_id).all()


def create_asset(db: Session, asset: schemas.AssetCreate):
    db_asset = models.Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


def create_tick(db: Session, tick: schemas.TickCreate):
    # Find the latest tick to determine the next tick number and to get assets from
    latest_tick = (
        db.query(models.Tick)
        .filter(models.Tick.campaign_id == tick.campaign_id)
        .order_by(models.Tick.tick_number.desc())
        .first()
    )

    next_tick_number = 1
    if latest_tick:
        next_tick_number = latest_tick.tick_number + 1

    # Create the new tick
    db_tick = models.Tick(
        campaign_id=tick.campaign_id,
        tick_number=next_tick_number,
        narrative=tick.narrative,
    )
    db.add(db_tick)
    db.commit()
    db.refresh(db_tick)

    # If there was a previous tick, cascade its assets
    if latest_tick:
        assets_to_cascade = get_assets_by_tick_id(db, tick_id=latest_tick.id)
        for asset in assets_to_cascade:
            new_asset = models.Asset(
                tick_id=db_tick.id,
                asset_type=asset.asset_type,
                name=asset.name,
                description=asset.description,
                traits=asset.traits,
            )
            db.add(new_asset)
        db.commit() # Commit all new assets at once

    return db_tick


def generate_share_token_for_campaign(db: Session, campaign: models.Campaign):
    token = secrets.token_urlsafe(16)
    campaign.share_token = token
    db.commit()
    db.refresh(campaign)
    return token


def get_campaign_by_share_token(db: Session, token: str):
    return db.query(models.Campaign).filter(models.Campaign.share_token == token).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# @trace TASK-007
# @trace TASK-008
# @trace TASK-012
# @trace TASK-014
# @trace TASK-013
# @trace TASK-010
