from sqlalchemy.orm import Session

from . import models


def get_user(username: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        return None
    else:
        return user


def get_user_by_id(id: str, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        return None
    else:
        return user
