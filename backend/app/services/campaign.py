# @trace TASK-016
from sqlalchemy.orm import Session
from app.models import Campaign
from app.schemas import CampaignCreate
from app.services import timeline
import uuid

def create_campaign(db: Session, gm_user_id: int, campaign_data: CampaignCreate) -> Campaign:
    db_campaign = Campaign(
        gm_user_id=gm_user_id,
        name=campaign_data.name,
        description=campaign_data.description,
        party_size=campaign_data.party_size,
        party_level=campaign_data.party_level
    )
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)

    # Initialize the timeline by creating the first tick
    timeline.initialize_timeline(db, db_campaign.id)

    return db_campaign

def generate_share_link(db: Session, campaign_id: int, base_url: str) -> str:
    db_campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not db_campaign:
        return None

    if not db_campaign.share_token:
        db_campaign.share_token = str(uuid.uuid4())
        db.commit()
        db.refresh(db_campaign)

    return f"{base_url.rstrip('/')}/share/{db_campaign.share_token}"

def get_shared_campaign(db: Session, share_token: str) -> Campaign:
    return db.query(Campaign).filter(Campaign.share_token == share_token).first()
