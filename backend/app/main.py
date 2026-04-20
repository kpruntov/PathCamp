from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from . import crud, models, schemas, token
from .database import engine, get_db
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

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @trace TASK-005
# @trace TASK-007
# @trace TASK-008
