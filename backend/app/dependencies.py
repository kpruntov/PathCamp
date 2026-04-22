from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import crud, schemas, token
from .database import get_db

# @trace TASK-009

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    db: Session = Depends(get_db), token_str: str = Depends(oauth2_scheme)
) -> schemas.User:
    """
    Dependency to get the current user from a token.
    Decodes the token, validates the user, and returns the user object.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = token.verify_token(token_str, credentials_exception)

    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception

    return user


def get_admin_user(current_user: schemas.User = Depends(get_current_user)):
    """
    Dependency that checks if the current user is an admin.
    """
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have enough privileges",
        )
    return current_user

# @trace TASK-010
