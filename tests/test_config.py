import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_secret_key(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://x")
    monkeypatch.delenv("SECRET_KEY", raising=False)
    with pytest.raises(ValidationError, match="secret_key"):
        Settings(_env_file=None)
