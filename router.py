from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import auth
from database import schemas, crud
from database.database import get_db

api_router = APIRouter()


@api_router.get("/whoisthat")
async def whoisthat(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user


@api_router.post("/add_weight")
async def add_weight(weight: schemas.WeightBase, user: schemas.User = Depends(auth.get_current_user),
                     db: Session = Depends(get_db)):
    return crud.add_new_weight(weight, user.id, db=db)
