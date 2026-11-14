import time

STARTED_AT = time.monotonic()


def get_status() -> dict[str, str]:
    return {"status": "ok"}


def get_uptime() -> dict[str, int]:
    return {"uptime_seconds": int(time.monotonic() - STARTED_AT)}
