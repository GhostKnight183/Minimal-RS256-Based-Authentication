from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
from core import get_db_session, check_pass, set_cookie, create_access, create_refresh,AsyncSession
from shemas import users_login, Token_Info
from models import UsersOrm

router = APIRouter(tags=["Registration"])

async def valide_login(stored_users:users_login,session: AsyncSession = Depends(get_db_session)):
    query = (
        select(UsersOrm)
        .filter(UsersOrm.username == stored_users.username)
    )
    result = await session.execute(query)
    stored_user = result.scalars().first()

    if not stored_user or not check_pass(stored_users.password, stored_user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    return stored_user

@router.post("/login", response_model=Token_Info)
async def user_login(stored_user: users_login = Depends(valide_login)):
    access_token = create_access(stored_user)
    refresh_token = create_refresh(stored_user)

    response = JSONResponse(content={"mesage": "Login successful"})

    set_cookie(response, "access_token", access_token, 60*15)
    set_cookie(response, "refresh_token", refresh_token, 60*24*3600)

    return response
