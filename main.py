from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import routers
from config import settings
from tortoise.contrib.fastapi import register_tortoise


app = FastAPI(title='Documentation',
              description="",
              version="0.1.0",)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=settings.CORS_ORIGINS,  #Проверить
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/home")
async def hello():
    return {"Hello":"World"}


app.include_router(routers.api_router, prefix='/api/v1')


register_tortoise(
    app,
    db_url=settings.DB_URL,
    modules={"models": settings.APPS_MODEL},
    generate_schemas=True,
    add_exception_handlers=True,
)