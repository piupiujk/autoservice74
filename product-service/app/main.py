from fastapi import FastAPI

from app.api import router

app = FastAPI(title='Product Service')

app.include_router(router)
