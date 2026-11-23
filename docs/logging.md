# Logging

The API writes one log line for every request, shows it in the terminal, and keeps the important lines in a file.

```
2026-11-23 20:54:55,029 INFO     feito.access: GET /api/health 200 4.1ms
2026-11-23 20:54:55,042 WARNING  feito.access: GET /api/naoexiste 404 0.6ms
```

Each line has the time, the level, the logger name, and the message. For requests the message is: method, path, status code, and duration.

The code lives in `app/utils/log/`:

| File | What it does |
|---|---|
| `logger.py` | `setup_logging`: configures the terminal output, the file, the colors, and the filter |
| `middleware.py` | Logs every request, with the level chosen from the status code |

`setup_logging` runs once, in `app/main.py`, when the API starts.

## Levels

A level says how important a message is. The terminal shows messages from the chosen level up.

| Level | Meaning | Color |
|---|---|---|
| `DEBUG` | Fine detail, for debugging | cyan |
| `INFO` | Normal events | green |
| `WARNING` | Something odd, but it continues | yellow |
| `ERROR` | Something failed | red |
| `CRITICAL` | The system cannot continue | bold red |

Requests get their level from the response status:

| Status | Level |
|---|---|
| 2xx and 3xx | `INFO` |
| 4xx | `WARNING` |
| 5xx | `ERROR` |

## `LOG_LEVEL`

The `LOG_LEVEL` variable in `.env` sets the lowest level the **terminal** shows. The default is `INFO`, and the accepted values are `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`. Any other value stops the API at startup with a clear error.

| Environment | Suggested value |
|---|---|
| Your machine | `INFO`, or `DEBUG` to see everything |
| Production | `INFO` or `WARNING` |
| Hunting a bug | `DEBUG` for a while |

Restart the API after changing it.

## Terminal and file

| | Terminal | File `logs/feito.log` |
|---|---|---|
| **Which messages** | From `LOG_LEVEL` up | `WARNING` and above, plus any message marked with `to_file` |
| **Colors** | Yes, only in a real terminal | Never |
| **Controlled by `LOG_LEVEL`** | Yes | No, it has its own rule |

- **Colors** are turned off when the output is not a terminal (for example, redirected to a file) and when the `NO_COLOR` environment variable exists.
- **The file** is created automatically, together with the `logs/` folder, when the API starts. The path is relative to the folder where you run the command, so run it from the project root (`make run` does). The folder is ignored by git.
- **Rotation:** when the file reaches 1 MB, a new one starts, and the 3 previous ones are kept. The file never grows without limit.

## Writing your own log messages

Create a logger once at the top of the file, and call it where you need it:

```python
import logging

logger = logging.getLogger(__name__)


def something(email: str) -> None:
    logger.info("user %s opened the list", email)        # terminal only
    logger.warning("login failed for %s", email)          # terminal and file
```

`__name__` is the module name, such as `app.modules.auth.service`, and it appears in the line, so you can see where a message came from.

To record an error with its full stack trace, use `logger.exception` inside an `except` block:

```python
try:
    send_email(user)
except Exception:
    logger.exception("could not send the email to %s", user.email)
```

### Saving a message in the file on purpose

By default only `WARNING` and above reach the file. To keep a lower-level message, such as a sensitive action, mark it:

```python
logger.info("user %s changed the password", email, extra={"to_file": True})
```

The mark works at any level, and it also works when `LOG_LEVEL` is higher than the message: with `LOG_LEVEL=WARNING` the line is hidden in the terminal but is still saved in the file.

### Rules for messages

- **Pass values as arguments, not in an f-string:** `logger.warning("login failed for %s", email)`. The text is only built if the message is really written.
- **Never log secrets.** No passwords, tokens, `SECRET_KEY`, or request bodies. Log who did what, and the result. The log file has no protection, and anyone who opens it reads everything.

## Why the query string is never logged

The email confirmation link looks like `/auth/confirm-email?token=...`: the token travels in the URL, after the `?`. The middleware logs only the path (`request.url.path`), so the token never reaches the log.

For the same reason the API runs with `--no-access-log` (already set in `make run`). The access log that uvicorn writes by itself contains the full URL, token included, and it would duplicate the line the middleware already writes.

## Limits

- **Unhandled errors (500) are not logged yet.** When a route crashes, the exception skips the middleware. Logging them is the job of the "Erros padronizados e handler global" card, which will use this same logger.
- **The file rotation is not safe with several server processes** writing at the same time. With one process, as in development, it is fine. In production with several workers, send the logs to a log service instead.
- **Access logs are plain text.** A structured format (JSON) and a request id are left for the deploy.

## Tests

`tests/test_logging.py` covers the request line, the missing query string, the `WARNING` level for 4xx, the colors, and the file filter. See [testing.md](testing.md).
