from db_set import setting
from datetime import timedelta
from models import UsersOrm
from fastapi.responses import JSONResponse
import bcrypt
import datetime
import jwt

access_token : str = "acces_token"
refresh_token : str = "refresh_token"

private_key = setting.private_key.read_text()
public_key = setting.public_key.read_text()


def gen_salt(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_pass(password:str,hashed_password:bytes) -> bool:
    return bcrypt.checkpw(password.encode(),hashed_password)


def encode_token(payload:dict,expire_token_time = setting.access_token_time,expire_token_timedelta: timedelta|None = None):
    now = datetime.datetime.utcnow()
    if expire_token_timedelta:
        exp = now + expire_token_timedelta
    else:
        exp = now + timedelta(minutes=expire_token_time)
    
    payload.update({
        "iat":now,
        "exp":exp
    })
    return jwt.encode(
        payload,
        private_key,
        algorithm=setting.algorithms
    )


def decode_token(token:str):
    return jwt.decode(
        token,
        public_key,
        algorithms=setting.algorithms
    )


def create_token(payload:dict,expire_minuts:int|None = None,expire_timedelta : timedelta|None = None):
    return encode_token(
        payload = payload.copy(),
        expire_token_time= expire_minuts,
        expire_token_timedelta=expire_timedelta
     )


def create_access(stored_user : UsersOrm):
    return create_token(
        payload = {
            "token_type" : access_token,
            "sub": stored_user.username,
            "user_id": stored_user.id,
            "email": stored_user.email,
            "is_admin": stored_user.is_admin

        },
        expire_minuts = setting.access_token_time
    )

def create_refresh(stored_user:UsersOrm):
    return create_token(
        payload = {
            "token_type": refresh_token,
            "user_id": stored_user.id,
            "email": stored_user.email
        },
        expire_timedelta = timedelta(days=setting.refresh_token_time)
    )



def set_cookie(response : JSONResponse,key: str,value : str,max_age:int):
    response.set_cookie(
        key= key,
        value=value,
        httponly= True,
        samesite="strict",
        secure= True,
        max_age= max_age,
    )
    