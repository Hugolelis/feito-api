import logging

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from app.core.errors import AppError, register_error_handlers
from app.main import app


class Signup(BaseModel):
    password: str = Field(min_length=8)


def make_client() -> TestClient:
    mini = FastAPI()
    register_error_handlers(mini)

    @mini.get("/domain")
    def domain() -> None:
        raise AppError(409, "EMAIL_ALREADY_EXISTS", "E-mail already registered")

    @mini.post("/signup")
    def signup(body: Signup) -> None:
        return None

    @mini.get("/boom")
    def boom() -> None:
        raise RuntimeError("internal secret")

    # Starlette re-raises after the 500 handler answers; this flag keeps the response
    return TestClient(mini, raise_server_exceptions=False)


def test_app_error() -> None:
    """A business error answers with its own status and {code, message}."""
    r = make_client().get("/domain")
    assert r.status_code == 409
    assert r.json() == {"code": "EMAIL_ALREADY_EXISTS", "message": "E-mail already registered"}


def test_validation_error() -> None:
    """Invalid data gives 422 with the failing field, and never echoes what was sent."""
    r = make_client().post("/signup", json={"password": "weak"})
    body = r.json()
    assert r.status_code == 422
    assert body["code"] == "VALIDATION_ERROR"
    assert body["details"][0]["field"] == "body.password"
    assert "weak" not in r.text


def test_not_found() -> None:
    """Framework errors, like an unknown route, use the same {code, message} format."""
    r = TestClient(app).get("/api/noexist")
    assert r.status_code == 404
    assert r.json() == {"code": "NOT_FOUND", "message": "Not Found"}


def test_unexpected_error(caplog) -> None:
    """A bug gives a generic 500 without details, and the real error goes to the log."""
    with caplog.at_level(logging.ERROR):
        r = make_client().get("/boom")
    assert r.status_code == 500
    assert r.json() == {"code": "INTERNAL_ERROR", "message": "Internal server error"}
    assert "internal secret" not in r.text
    assert "RuntimeError" in caplog.text
