from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

import auth
from config.config import config
from database import schemas
from database.database import get_db
from router import api_router

docs_kwargs = {}
if config['ENVIRONMENT'] == 'production':
    docs_kwargs = dict(docs_url=None, redoc_url=None)

app = FastAPI(**docs_kwargs)


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


app.include_router(api_router, dependencies=[Depends(auth.get_current_user)])


# @app.get("/users/me/", response_model=schemas.User)
# async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
#     return current_user
