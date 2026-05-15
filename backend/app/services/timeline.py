# @trace TASK-021
from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, status

def get_timeline(db: Session, campaign_id: int) -> schemas.TimelineData:
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    
    # We could optimize this query, but for now we rely on SQLAlchemy relationships
    ticks = db.query(models.Tick).filter(models.Tick.campaign_id == campaign_id).order_by(models.Tick.tick_number.asc()).all()
    
    # We map it to our schema
    return schemas.TimelineData(
        campaign_id=campaign_id,
        ticks=[
            schemas.TickResponse.model_validate(tick) for tick in ticks
        ]
    )

def initialize_timeline(db: Session, campaign_id: int) -> models.Tick:
    """
    Initializes the timeline by creating the first tick.
    """
    tick = models.Tick(
        campaign_id=campaign_id,
        tick_number=1,
        narrative="Campaign started."
    )
    db.add(tick)
    db.commit()
    db.refresh(tick)
    return tick

def create_next_tick(db: Session, campaign_id: int, narrative: str) -> int:
    """
    Calculates state to cascade from the previous tick and persists the new tick.
    """
    # 1. Find the latest tick
    latest_tick = db.query(models.Tick).filter(
        models.Tick.campaign_id == campaign_id
    ).order_by(models.Tick.tick_number.desc()).first()
    
    if not latest_tick:
        # Fallback if uninitialized
        new_tick_number = 1
    else:
        new_tick_number = latest_tick.tick_number + 1

    # 2. Create the new tick
    new_tick = models.Tick(
        campaign_id=campaign_id,
        tick_number=new_tick_number,
        narrative=narrative
    )
    db.add(new_tick)
    db.flush() # Get new_tick.id without committing yet
    
    # 3. Cascade assets from the previous tick
    if latest_tick:
        for old_asset in latest_tick.assets:
            new_asset = models.Asset(
                tick_id=new_tick.id,
                asset_type=old_asset.asset_type,
                name=old_asset.name,
                description=old_asset.description,
                traits=old_asset.traits
            )
            db.add(new_asset)
            db.flush()
            # Note: We are not cascading encounters directly unless needed. 
            # Encounters are usually specific to a tick.
            
    db.commit()
    return new_tick.id

def update_tick(db: Session, tick_id: int, narrative: str) -> bool:
    tick = db.query(models.Tick).filter(models.Tick.id == tick_id).first()
    if not tick:
        return False
    
    tick.narrative = narrative
    db.commit()
    return True

def create_asset_in_tick(db: Session, tick_id: int, asset_data: schemas.AssetCreate) -> models.Asset:
    asset = models.Asset(
        tick_id=tick_id,
        **asset_data.model_dump()
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

def update_asset_in_tick(db: Session, asset_id: int, asset_data: schemas.AssetCreate) -> bool:
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        return False
    
    for key, value in asset_data.model_dump().items():
        setattr(asset, key, value)
        
    db.commit()
    return True

def save_encounter_to_tick(db: Session, asset_id: int, encounter_data: schemas.EncounterCreate) -> bool:
    # Ensure asset exists
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        return False
        
    encounter = models.Encounter(
        asset_id=asset_id,
        **encounter_data.model_dump()
    )
    db.add(encounter)
    db.commit()
    return True
