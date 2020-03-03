from fastapi import FastAPI, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

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
        raise auth.credentials_exception

    access_token = auth.create_access_token(
        data={"sub": user.username}
    )
    refresh_token = auth.create_refresh_token(
        data={"sub": user.id}
    )

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@app.post("/renew_token", response_model=schemas.Token)
async def renew_token(*, r_token: str = Header(None), db: Session = Depends(get_db)):
    user = auth.check_refresh_token(db, token=r_token)
    if not user:
        raise auth.credentials_exception

    access_token = auth.create_access_token(
        data={"sub": user.username}
    )
    refresh_token = auth.create_refresh_token(
        data={"sub": user.id}
    )

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


app.include_router(api_router, dependencies=[Depends(auth.get_current_user)])

# @app.get("/users/me/", response_model=schemas.User)
# async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
#     return current_user
