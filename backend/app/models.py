from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    status = Column(String, nullable=False, server_default="Active")
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    gm_user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    party_size = Column(Integer, nullable=False)
    party_level = Column(Integer, nullable=False)
    share_token = Column(String(255), unique=True, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    owner = relationship("User")


# @trace TASK-007
# @trace TASK-012
