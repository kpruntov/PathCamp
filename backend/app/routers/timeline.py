# @trace TASK-022
# @trace TASK-044
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import SessionLocal
from app.dependencies import get_db, get_current_active_user, get_optional_user
from app.services import timeline

router = APIRouter(tags=["timeline"])

def check_campaign_ownership(db: Session, campaign_id: int, user_id: int):
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    if campaign.gm_user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this campaign")

def check_tick_ownership(db: Session, tick_id: int, user_id: int):
    tick = db.query(models.Tick).filter(models.Tick.id == tick_id).first()
    if not tick:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tick not found")
    check_campaign_ownership(db, tick.campaign_id, user_id)

@router.get("/campaigns/{campaignId}/timeline", response_model=schemas.TimelineData)
def get_campaign_timeline(campaignId: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_optional_user)):
    data = timeline.get_timeline(db, campaign_id=campaignId)
    # Check if current user is owner
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaignId).first()
    is_owner = False
    if campaign and current_user and campaign.gm_user_id == current_user.id:
        is_owner = True
    
    return schemas.TimelineData(
        campaign_id=data.campaign_id,
        is_owner=is_owner,
        ticks=data.ticks
    )

@router.post("/ticks", status_code=status.HTTP_201_CREATED)
def create_next_tick(tick_data: schemas.TickCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    check_campaign_ownership(db, tick_data.campaign_id, current_user.id)
    # Using the timeline service to create the next tick
    new_tick_id = timeline.create_next_tick(db, campaign_id=tick_data.campaign_id, narrative=tick_data.narrative)
    return {"new_tick_id": new_tick_id}

@router.put("/ticks/{tickId}")
def update_tick(tickId: int, tick_data: schemas.TickBase, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    check_tick_ownership(db, tickId, current_user.id)
    success = timeline.update_tick(db, tick_id=tickId, narrative=tick_data.narrative)
    if not success:
        raise HTTPException(status_code=404, detail="Tick not found")
    return {"success": True}

@router.post("/ticks/{tickId}/assets", status_code=status.HTTP_201_CREATED)
def create_asset_in_tick(tickId: int, asset_data: schemas.AssetCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    check_tick_ownership(db, tickId, current_user.id)
    asset = timeline.create_asset_in_tick(db, tick_id=tickId, asset_data=asset_data)
    return {"asset_id": asset.id}

@router.post("/ticks/{tickId}/scenes/{sceneId}/encounter")
def save_encounter_to_tick(tickId: int, sceneId: int, encounter_data: schemas.EncounterCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    check_tick_ownership(db, tickId, current_user.id)
    success = timeline.save_encounter_to_tick(db, asset_id=sceneId, encounter_data=encounter_data)
    if not success:
        raise HTTPException(status_code=404, detail="Scene asset not found")
    return {"success": True}
