from fastapi import FastAPI, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

'''import motor.motor_asyncio as motor'''
import asyncpg

from contextlib import asynccontextmanager

#from logs import api_logging
#from postgresql import engine

'''from config import (
    MONGO_DATABASE_URL,
    MONGO_DATABASE_NAME,
    POSTGRES_DATABASE_URL,
    REDIS_CACHE_URL,
    SMTP_HOST,
    SMTP_PORT,
    SMTP_EMAIL,
    SMTP_PASSWORD,
)'''
#from routes.mongo.routes import router as mongo_router
#from routes.postgres.routes import router as postgres_router
from .auth.ident.routes import router as auth_router
#from auth.ident.manager import get_current_active_user
#from auth.register.routes import router as register_router
#from auth.res_forgot_passwd.routes import router as res_forgot_passwd
#from auth.res_forgot_passwd.redis.redis import RedisTools
#from auth.res_forgot_passwd.smtp.smtp import SmtpTools
#from auth.user.routes import router as users_router
#from auth.role.routes import router as role_router


'''@asynccontextmanager
async def lifespan(api: FastAPI):
    api.mongodb_client = motor.AsyncIOMotorClient(MONGO_DATABASE_URL)
    api.database = api.mongodb_client[MONGO_DATABASE_NAME]

    api.postgresql = await asyncpg.create_pool(POSTGRES_DATABASE_URL)

    api.redis = RedisTools(url=REDIS_CACHE_URL)

    api.smtp = SmtpTools(SMTP_HOST, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD)
    try:
        yield
    finally:
        api.mongodb_client.close()
        await api.postgresql.close()
        await api.redis.close()
        api.smtp.__del__()'''


app = FastAPI(title="Web_Example_Project", version="0.5.2",) #lifespan=lifespan)


"""@app.middleware("http")
async def logging_middleware(request: Request, call_next) -> Response:
    async with AsyncSession(engine) as postgres_session:
        return await api_logging(request, call_next, postgres_session)"""


app.include_router(auth_router, tags=["auth"], prefix="/auth")
'''app.include_router(register_router, tags=["auth"], prefix="/auth")
app.include_router(res_forgot_passwd, tags=["auth"], prefix="/auth")

app.include_router(users_router, tags=["users"], prefix="/users")

app.include_router(role_router, tags=["role"], prefix="/role")

app.include_router(mongo_router, tags=["mongo"], prefix="/mongo")

app.include_router(
    postgres_router,
    tags=["postgres"],
    prefix="/postgres",
    dependencies=[Depends(get_current_active_user)],
)
'''