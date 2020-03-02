from fastapi import Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db


def get_user(username: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        return None
    else:
        return user
