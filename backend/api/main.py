from fastapi import FastAPI, Depends
import motor.motor_asyncio as motor
import asyncpg

from config import MONGO_DATABASE_URL, MONGO_DATABASE_NAME, POSTGRES_DATABASE_URL
from routes.mongo.routes import router as mongo_router
from routes.postgres.routes import router as postgres_router
from routes.auth.ident.routes import router as auth_router
from routes.auth.ident.manager import get_current_active_user
from routes.auth.register.routes import router as register_router
from routes.auth.res_forgot_passwd.routes import router as res_forgot_passwd
from routes.auth.user.routes import router as users_router
from routes.auth.role.routes import router as role_router


app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = motor.AsyncIOMotorClient(MONGO_DATABASE_URL)
    app.database = app.mongodb_client[MONGO_DATABASE_NAME]
    print("Connected to the MongoDB database!")

    app.postgresql = await asyncpg.connect(POSTGRES_DATABASE_URL)
    print("Connected to the Postgresql database!")


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
    await app.postgresql.close()


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
