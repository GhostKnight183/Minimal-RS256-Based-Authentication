from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from core import set_cookie, AsyncSession, get_db_session, decode_token, create_access
from models import UsersOrm
from sqlalchemy import select
from shemas import Token_Info
import jwt

router = APIRouter()

@router.post("/refresh-token")
async def refresh_access_token(request: Request, session: AsyncSession = Depends(get_db_session)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token required")

    try:
        payload = decode_token(refresh_token)
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        query = select(UsersOrm).filter(UsersOrm.id == user_id)
        result = await session.execute(query)
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        access_token = create_access(user)
        response = JSONResponse(content={"message": "Token refreshed"})
        set_cookie(response, "access_token", access_token, 60 * 15)

        return response
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
