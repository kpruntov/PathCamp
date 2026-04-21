from sqlalchemy.orm import Session
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


def create_campaign(db: Session, campaign: schemas.CampaignCreate, gm_user_id: int):
    db_campaign = models.Campaign(**campaign.model_dump(), gm_user_id=gm_user_id)
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    # TODO: Initialize timeline with Tick 1 (FR-003)
    return db_campaign


# @trace TASK-007
# @trace TASK-008
# @trace TASK-012
