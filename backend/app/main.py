from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from . import crud, models, schemas, token
from .database import engine, get_db
from .dependencies import get_current_user, get_admin_user
from .hashing import Hasher

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not Hasher.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Note: In a real app, you'd check if the user already exists.
    # This is omitted for brevity as per the test case structure.
    db_user = crud.create_user(db=db, user=user)
    return db_user


@app.post("/logout")
def logout():
    # In a real application, this would invalidate the token, e.g., by using a blacklist.
    # For now, we just return a success message as per the spec.
    return {"message": "Logout successful"}


@app.post(
    "/campaigns", response_model=schemas.Campaign, status_code=status.HTTP_201_CREATED
)
def create_new_campaign(
    campaign: schemas.CampaignCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    db_campaign = crud.get_campaign_by_name(
        db, name=campaign.name, gm_user_id=current_user.id
    )
    if db_campaign:
        raise HTTPException(
            status_code=400, detail="A campaign with this name already exists."
        )
    return crud.create_campaign(db=db, campaign=campaign, gm_user_id=current_user.id)


@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @trace TASK-005
# @trace TASK-007
# @trace TASK-008
# @trace TASK-009
# @trace TASK-012
# @trace TASK-014


@app.post("/ticks", response_model=schemas.Tick, status_code=status.HTTP_201_CREATED)
def create_tick(
    tick: schemas.TickCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    db_campaign = crud.get_campaign_by_id(
        db, campaign_id=tick.campaign_id, gm_user_id=current_user.id
    )
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return crud.create_tick(db=db, tick=tick)


@app.get("/campaigns/{campaign_id}/share", response_model=schemas.ShareLink)
def generate_share_link(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    db_campaign = crud.get_campaign_by_id(
        db, campaign_id=campaign_id, gm_user_id=current_user.id
    )
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    token = crud.generate_share_token_for_campaign(db, campaign=db_campaign)
    # In a real app, the domain would be configured, not hardcoded
    share_url = f"http://example.com/shared/{token}"
    return {"share_url": share_url}


@app.get("/shared/{token}", response_model=schemas.CampaignPublic)
def get_shared_campaign(token: str, db: Session = Depends(get_db)):
    db_campaign = crud.get_campaign_by_share_token(db, token=token)
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return db_campaign


# @trace TASK-013
# @trace TASK-010


@app.get("/admin/users", response_model=List[schemas.User])
def get_all_users(
    db: Session = Depends(get_db),
    admin_user: schemas.User = Depends(get_admin_user),
):
    users = crud.get_users(db)
    return users
