from pydantic import BaseModel,EmailStr
from typing import Annotated

class users_register(BaseModel):
    email : Annotated[str,EmailStr]
    username : str
    password : str

class users_login(BaseModel):
    username: str
    password: str