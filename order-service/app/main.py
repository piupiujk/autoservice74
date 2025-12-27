from fastapi import FastAPI

from app.api import router

app = FastAPI(title='Order Service')

app.include_router(router)
