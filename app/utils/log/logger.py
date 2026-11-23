import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"
LOG_FILE = Path("logs/feito.log")

RESET = "\033[0m"
COLORS = {
    logging.DEBUG: "\033[36m",  # cyan
    logging.INFO: "\033[32m",  # green
    logging.WARNING: "\033[33m",  # yellow
    logging.ERROR: "\033[31m",  # red
    logging.CRITICAL: "\033[1;31m",  # bold red
}


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        color = COLORS.get(record.levelno, "")
        return f"{color}{super().format(record)}{RESET}"


class FileFilter(logging.Filter):
    """The file keeps WARNING and above, plus any record marked with extra={"to_file": True}."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno >= logging.WARNING or getattr(record, "to_file", False)


def setup_logging(level: str) -> None:
    numeric = logging.getLevelNamesMapping()[level]

    # terminal: everything from `level` up, colored only when it is a real terminal
    console = logging.StreamHandler()
    console.setLevel(numeric)
    colored = sys.stderr.isatty() and "NO_COLOR" not in os.environ
    console.setFormatter(ColorFormatter(LOG_FORMAT) if colored else logging.Formatter(LOG_FORMAT))

    # file: only what is important, plain text, rotated
    # ponytail: rotation is not safe with several worker processes; use a log service then
    LOG_FILE.parent.mkdir(exist_ok=True)
    file = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    file.addFilter(FileFilter())
    file.setFormatter(logging.Formatter(LOG_FORMAT))

    # the root logger must let INFO through even when `level` is higher,
    # or a marked INFO would never reach the file; each handler filters on its own
    logging.basicConfig(level=min(numeric, logging.INFO), handlers=[console, file])
