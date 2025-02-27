from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy import select
from core import get_db_session,gen_salt
from shemas import users_register
from models import UsersOrm
from core import AsyncSession

router = APIRouter( tags=["Registration"])


async def valide_register(stored_user: users_register, session: AsyncSession = Depends(get_db_session)):
    query = (
        select(UsersOrm)
        .filter((UsersOrm.username == stored_user.username) | (UsersOrm.email == stored_user.email))
    )
    result = await session.execute(query)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code = 400,detail= "User alredy register")
    
    return stored_user


@router.post("/register")
async def user_register(user: users_register = Depends(valide_register), session: AsyncSession = Depends(get_db_session)):
    hashed_password = gen_salt(user.password)
    new_user = UsersOrm(email=user.email, username=user.username, password=hashed_password, is_admin=False)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {"email": new_user.email, "username": new_user.username}