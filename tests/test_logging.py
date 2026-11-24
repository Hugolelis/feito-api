import logging

from fastapi.testclient import TestClient

from app.main import app
from app.utils.log.logger import ColorFormatter, FileFilter

client = TestClient(app)


def test_request_log(caplog) -> None:
    """Each request writes one line with method, path, and status."""
    with caplog.at_level(logging.INFO, logger="feito.access"):
        client.get("/api/health")
    assert "GET /api/health 200" in caplog.text


def test_no_query_string(caplog) -> None:
    """The query string (where the email token travels) never reaches the log."""
    with caplog.at_level(logging.INFO, logger="feito.access"):
        client.get("/api/health?token=segredo123")
    assert "segredo123" not in caplog.text


def test_4xx_warning(caplog) -> None:
    """A 4xx response is logged as WARNING."""
    with caplog.at_level(logging.INFO, logger="feito.access"):
        client.get("/api/naoexiste")
    record = next(r for r in caplog.records if "naoexiste" in r.message)
    assert record.levelno == logging.WARNING


def test_color_formatter() -> None:
    """The formatter wraps the line in the color of its level."""
    record = logging.LogRecord("x", logging.WARNING, "", 0, "oi", None, None)
    assert ColorFormatter("%(message)s").format(record) == "\033[33moi\033[0m"


def test_file_filter() -> None:
    """The file keeps WARNING and above, and any record marked with to_file."""
    file_filter = FileFilter()
    info = logging.LogRecord("x", logging.INFO, "", 0, "m", None, None)
    assert not file_filter.filter(info)
    info.to_file = True
    assert file_filter.filter(info)
    warning = logging.LogRecord("x", logging.WARNING, "", 0, "m", None, None)
    assert file_filter.filter(warning)
