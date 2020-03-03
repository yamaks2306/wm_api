from datetime import datetime

from sqlalchemy.orm import Session

from . import models, schemas


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


def add_new_weight(weight: schemas.WeightBase, user: str, db: Session):
    timestamp = int(datetime.now().timestamp())

    db_weight = models.Weight(Timestamp=timestamp, user=user, weight=weight.weight)
    db.add(db_weight)
    db.commit()
    db.refresh(db_weight)
    return db_weight
