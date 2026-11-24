from fastapi import APIRouter, FastAPI

from app.core.config import settings
from app.core.errors import register_error_handlers
from app.modules.health.router import router as health_router
from app.utils.log.logger import setup_logging
from app.utils.log.middleware import log_requests

setup_logging(settings.log_level)

routers = [
    health_router,
]

api = APIRouter(prefix="/api")
for router in routers:
    api.include_router(router)

app = FastAPI(title="Feito API")
register_error_handlers(app)
app.middleware("http")(log_requests)
app.include_router(api)
