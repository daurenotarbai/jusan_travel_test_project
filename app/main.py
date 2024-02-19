from fastapi import FastAPI

from app import database
from app.api.user import router as user_router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Jusan Travel Test Task API",
    description="API для регистрации и авторизации пользователей",
    version="1.0.0",
    contact={
        "name": "Даурен Отрабай",
        "email": "daurenotarbai.00@gmail.com",
    },
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)


@app.on_event('startup')
async def startup():
    await database.initialize()


@app.on_event('shutdown')
async def shutdown():
    await database.close_connections()


app.include_router(user_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
