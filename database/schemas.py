from pydantic import BaseModel


class WeightBase(BaseModel):
    weight: float


class WeightCreate(WeightBase):
    pass


class Weight(WeightBase):
    id: str
    owner: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    password: str
    email: str
    Timestamp: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str

    # weights: List[Weight] = []

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
    id: str
