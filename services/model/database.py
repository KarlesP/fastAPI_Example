from pydantic import BaseModel
from tinydb import TinyDB,Query
from pydantic import BaseModel, validator
from passlib.hash import bcrypt
from passlib.context import CryptContext

import os

def getDB(name):
   files = [f for f in os.listdir('.') if os.path.isfile(f)]
   db=name
   if not("name" in files):
       db = TinyDB(name)
   return (db)


class User(BaseModel):
    email: str
    password: str

    @validator('email')
    def email_valid(cls, value):
        assert '@' in value, 'invalid email'
        return value.lower()


class TokenData(BaseModel):
    sub: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserInDB(BaseModel):
    email: str
    hashed_password: str

    def check_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)


def getDB(name='users.json'):
   files = [f for f in os.listdir('.') if os.path.isfile(f)]
   db = name
   if not ("name" in files):
       db = TinyDB(name)
   return (db)


def create_user(user: User):
    user_dict = user.dict()
    user_dict['password'] = bcrypt.hash(user.password)
    users_table.insert(user_dict)
    return user


def get_user_by_email(email: str, whole=False):
    UserQuery = Query()
    user = users_table.get(UserQuery.email == email)
    if whole:
        return user
    else:
        return user['password']


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


db = TinyDB('users.json')
users_table = db.table('users')
tokens_table = db.table('tokens')
