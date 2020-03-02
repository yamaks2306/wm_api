from fastapi import APIRouter, Depends

import auth
from database import schemas

api_router = APIRouter()


@api_router.get("/whoisthat")
async def whoisthat(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user
