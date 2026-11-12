from fastapi import APIRouter, FastAPI

from app.modules.health.router import router as health_router

routers = [
    health_router,
]

api = APIRouter(prefix="/api")
for router in routers:
    api.include_router(router)

app = FastAPI(title="Feito")
app.include_router(api)