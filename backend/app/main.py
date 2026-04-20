from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Note: In a real app, you'd check if the user already exists.
    # This is omitted for brevity as per the test case structure.
    db_user = crud.create_user(db=db, user=user)
    return db_user

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @trace TASK-005
# @trace TASK-007
