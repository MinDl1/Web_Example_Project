from fastapi import FastAPI, Depends
import motor.motor_asyncio as motor
import asyncpg

from contextlib import asynccontextmanager

from config import (
    MONGO_DATABASE_URL,
    MONGO_DATABASE_NAME,
    POSTGRES_DATABASE_URL,
    REDIS_CACHE_URL,
    SMTP_HOST,
    SMTP_PORT,
    SMTP_EMAIL,
    SMTP_PASSWORD,
)
from routes.mongo.routes import router as mongo_router
from routes.postgres.routes import router as postgres_router
from routes.auth.ident.routes import router as auth_router
from routes.auth.ident.manager import get_current_active_user
from routes.auth.register.routes import router as register_router
from routes.auth.res_forgot_passwd.routes import router as res_forgot_passwd
from routes.auth.res_forgot_passwd.redis.redis import RedisTools
from routes.auth.res_forgot_passwd.smtp.smtp import SmtpTools
from routes.auth.user.routes import router as users_router
from routes.auth.role.routes import router as role_router


@asynccontextmanager
async def lifespan(api: FastAPI):
    api.mongodb_client = motor.AsyncIOMotorClient(MONGO_DATABASE_URL)
    api.database = api.mongodb_client[MONGO_DATABASE_NAME]

    api.postgresql = await asyncpg.connect(POSTGRES_DATABASE_URL)

    api.redis = RedisTools(url=REDIS_CACHE_URL)

    api.smtp = SmtpTools(SMTP_HOST, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD)
    try:
        yield
    finally:
        api.mongodb_client.close()
        await api.postgresql.close()
        await api.redis.close()
        api.smtp.__del__()


app = FastAPI(title="Web_Example_Project", version="0.5.2", lifespan=lifespan)


app.include_router(auth_router, tags=["auth"], prefix="/auth")
app.include_router(register_router, tags=["auth"], prefix="/auth")
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
