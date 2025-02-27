from core import get_db_session,access_token,decode_token,AsyncSession
from models import UsersOrm
from fastapi import Request,HTTPException,Depends
from sqlalchemy import select
import jwt


async def check_token(request: Request, session: AsyncSession = Depends(get_db_session)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        payload = decode_token(token)
        user_id = payload.get("user_id")
        email = payload.get("email")
        token_type = payload.get("token_type")

        if token_type != access_token:
            raise HTTPException(status_code=401, detail="Invalid token")
        if not user_id or not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    query = select(UsersOrm).filter(UsersOrm.id == user_id, UsersOrm.email == email)
    result = await session.execute(query)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    return 