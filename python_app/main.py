from fastapi import FastAPI
from api import user_login_router,user_register_router,refresh_token_router,test_token_router
from core import async_engine
from models import Base
import uvicorn

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(user_register_router)
app.include_router(user_login_router)
app.include_router(refresh_token_router)
app.include_router(test_token_router)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
