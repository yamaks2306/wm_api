from datetime import timedelta, datetime

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from config.config import config
from database import crud, schemas
from database.database import get_db

SECRET_KEY = config['TOKEN']['SECRET_KEY']
ALGORITHM = config['TOKEN']['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = config['TOKEN']['ACCESS_TOKEN_EXPIRE_MINUTES']
REFRESH_TOKEN_EXPIRE_MINUTES = config['TOKEN']['REFRESH_TOKEN_EXPIRE_MINUTES']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

credentials_exception = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_password(plain_password: str, hashed_password: str):
    return pbkdf2_sha256.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pbkdf2_sha256.hash(password)


def authenticate_user(db, username: str, password: str):
    user = crud.get_user(username=username, db=db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(*, data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(*, data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def check_refresh_token(db, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except PyJWTError:
        raise credentials_exception

    user = crud.get_user_by_id(token_data.id, db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except PyJWTError:
        raise credentials_exception

    user = crud.get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user
