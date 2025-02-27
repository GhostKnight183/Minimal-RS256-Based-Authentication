from db_set import setting
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession


async_engine = create_async_engine(setting.DB_asyncpg,echo = False)

async_sesion = async_sessionmaker(async_engine,class_= AsyncSession,expire_on_commit=False)


async def get_db_session():
    async with async_sesion() as session:
            yield session
            await session.commit()