from fastapi import FastAPI

from app.api import router

app = FastAPI(title='Автосервис 74')

app.include_router(router)
