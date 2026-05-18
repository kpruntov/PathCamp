# @trace TASK-017
# @trace TASK-042
# @trace TASK-043
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_active_user
from app.schemas import CampaignCreate, CampaignResponse, CampaignShareResponse, UserDetail
from app.services import campaign as campaign_service

router = APIRouter()

@router.get("/campaigns/all", response_model=List[CampaignResponse])
def get_all_campaigns(db: Session = Depends(get_db)):
    """Get all campaigns globally (public)."""
    return campaign_service.get_all_campaigns(db)

@router.get("/campaigns", response_model=List[CampaignResponse])
def get_campaigns(
    db: Session = Depends(get_db),
    current_user: UserDetail = Depends(get_current_active_user)
):
    """Get all campaigns for the current user."""
    return campaign_service.get_campaigns_by_gm(db, gm_user_id=current_user.id)

@router.post("/campaigns", response_model=CampaignResponse, status_code=201)
def create_campaign(
    campaign_in: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: UserDetail = Depends(get_current_active_user)
):
    """Create a new campaign."""
    campaign = campaign_service.create_campaign(db, gm_user_id=current_user.id, campaign_data=campaign_in)
    return campaign

@router.get("/campaigns/{campaign_id}/share", response_model=CampaignShareResponse)
def get_campaign_share_link(
    campaign_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: UserDetail = Depends(get_current_active_user)
):
    """Get a read-only share link for a campaign."""
    # Verify the campaign belongs to the current user
    from app.models import Campaign
    db_campaign = db.query(Campaign).filter(Campaign.id == campaign_id, Campaign.gm_user_id == current_user.id).first()
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    base_url = str(request.base_url)
    share_url = campaign_service.generate_share_link(db, campaign_id, base_url)
    if not share_url:
        raise HTTPException(status_code=500, detail="Failed to generate share link")
    return {"share_url": share_url}

@router.get("/shared/{share_token}", response_model=CampaignResponse)
def get_shared_campaign(
    share_token: str,
    db: Session = Depends(get_db)
):
    """Access a campaign via a share token."""
    campaign = campaign_service.get_shared_campaign(db, share_token)
    if not campaign:
        raise HTTPException(status_code=404, detail="Shared campaign not found")
    return campaign

@router.delete("/campaigns/{campaign_id}")
def delete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: UserDetail = Depends(get_current_active_user)
):
    """Delete a campaign."""
    success = campaign_service.delete_campaign(db, campaign_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Campaign not found or not authorized to delete")
    return {"success": True}
