# @trace TASK-022
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import SessionLocal
from app.dependencies import get_db, get_current_active_user
from app.services import timeline

router = APIRouter(tags=["timeline"])

@router.get("/campaigns/{campaignId}/timeline", response_model=schemas.TimelineData)
def get_campaign_timeline(campaignId: int, db: Session = Depends(get_db)):
    return timeline.get_timeline(db, campaign_id=campaignId)

@router.post("/ticks", status_code=status.HTTP_201_CREATED)
def create_next_tick(tick_data: schemas.TickCreate, db: Session = Depends(get_db)):
    # Using the timeline service to create the next tick
    new_tick_id = timeline.create_next_tick(db, campaign_id=tick_data.campaign_id, narrative=tick_data.narrative)
    return {"new_tick_id": new_tick_id}

@router.put("/ticks/{tickId}")
def update_tick(tickId: int, tick_data: schemas.TickBase, db: Session = Depends(get_db)):
    success = timeline.update_tick(db, tick_id=tickId, narrative=tick_data.narrative)
    if not success:
        raise HTTPException(status_code=404, detail="Tick not found")
    return {"success": True}

@router.post("/ticks/{tickId}/assets", status_code=status.HTTP_201_CREATED)
def create_asset_in_tick(tickId: int, asset_data: schemas.AssetCreate, db: Session = Depends(get_db)):
    asset = timeline.create_asset_in_tick(db, tick_id=tickId, asset_data=asset_data)
    return {"asset_id": asset.id}

@router.post("/ticks/{tickId}/scenes/{sceneId}/encounter")
def save_encounter_to_tick(tickId: int, sceneId: int, encounter_data: schemas.EncounterCreate, db: Session = Depends(get_db)):
    success = timeline.save_encounter_to_tick(db, asset_id=sceneId, encounter_data=encounter_data)
    if not success:
        raise HTTPException(status_code=404, detail="Scene asset not found")
    return {"success": True}
