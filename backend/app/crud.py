# @trace TASK-011
from sqlalchemy.orm import Session
from app import models, schemas, hashing
from sqlalchemy.exc import IntegrityError

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate, role: str = "GM"):
    hashed_password = hashing.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role=role
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        return None

def get_users(db: Session):
    return db.query(models.User).all()

def update_user_status(db: Session, user_id: int, status: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.status = status
        db.commit()
        db.refresh(db_user)
    return db_user
