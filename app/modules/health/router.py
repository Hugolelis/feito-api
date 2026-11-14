from fastapi import APIRouter

from app.modules.health import service

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health() -> dict[str, str]:
    return service.get_status()


@router.get("/uptime")
def uptime() -> dict[str, int]:
    return service.get_uptime()
