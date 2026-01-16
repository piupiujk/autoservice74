from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.proxy import router

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "API Gateway", "services": ["users", "products", "orders"]}

@app.get("/health")
async def health():
    return {"status": "ok"}