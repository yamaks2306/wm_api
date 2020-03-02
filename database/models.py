from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    DeletionMark = Column(Boolean, index=True)
    approved = Column(Boolean, index=True)
    Timestamp = Column(Integer, nullable=False, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, index=True)
    tid = Column(Integer, unique=True, index=True)

    # weights = relationship("Weight", back_populates="owner")


class Weight(Base):
    __tablename__ = "weight"

    id = Column(String, primary_key=True, index=True)
    Timestamp = Column(Integer, nullable=False, index=True)
    user = Column(String, ForeignKey("users.id"))
    weight = Column(Float, nullable=False, index=True)

    # owner = relationship("User", back_populates="weights")
