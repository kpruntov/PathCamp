# @trace TASK-010
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User
from sqlalchemy.exc import IntegrityError

@pytest.fixture(scope="module")
def engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

def test_create_user(db_session):
    new_user = User(
        username="test_admin",
        email="admin@test.com",
        password_hash="hashed_pw"
    )
    db_session.add(new_user)
    db_session.commit()
    
    assert new_user.id is not None
    assert new_user.status == "Active"
    assert new_user.created_at is not None
    assert new_user.updated_at is not None

def test_user_unique_constraints(db_session):
    user1 = User(username="unique_user", email="unique@test.com", password_hash="pw")
    db_session.add(user1)
    db_session.commit()

    user2 = User(username="unique_user", email="duplicate@test.com", password_hash="pw")
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    user3 = User(username="another_user", email="unique@test.com", password_hash="pw")
    db_session.add(user3)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
