from pydantic import BaseModel


class UserInput(BaseModel):
    email: str
    password: str


class UserRegisterInput(UserInput):
    username: str


class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True
