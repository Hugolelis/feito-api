# Tests

The tests use [pytest](https://pytest.org). They do not need Docker or a `.env` file.

```bash
make test
```

`make test` runs `poetry run pytest`. The project is configured to run pytest with `-v` (in `pyproject.toml`), so each test name is printed.

## Useful options

| Goal | Command |
|---|---|
| Stop at the first failure | `poetry run pytest -x` |
| One file | `poetry run pytest tests/test_health.py` |
| One test | `poetry run pytest tests/test_health.py::test_uptime` |
| Tests whose name contains a word | `poetry run pytest -k uptime` |
| Run the last failed tests again | `poetry run pytest --lf` |
| Lint, types, and tests together | `make check` |

## What is covered today

| File | What it checks |
|---|---|
| `tests/test_health.py` | `GET /api/health` returns 200 with `{"status": "ok"}`, and `GET /api/health/uptime` returns 200 with a non-negative `uptime_seconds` |
| `tests/test_config.py` | The settings refuse to load when a required variable is missing (`SECRET_KEY`), and the error names the variable |
| `tests/test_logging.py` | Each request produces a log line with method, path, and status; the query string (where the email token travels) is never logged; a 4xx response is logged as a `WARNING`; the color formatter colors by level; the log file keeps warnings and records marked with `extra={"to_file": True}` |

No test touches the database yet.

## How the tests get their configuration

`app/core/config.py` builds the settings as soon as it is imported, and it requires `DATABASE_URL` and `SECRET_KEY`. Without them, importing the app fails.

`tests/conftest.py` solves this. pytest loads it before any test file, and it sets dummy values for both variables:

```python
os.environ.setdefault("DATABASE_URL", "...")
os.environ.setdefault("SECRET_KEY", "chave-de-teste")
```

`setdefault` only fills a variable that does not exist yet, so a real value in your environment is never overwritten. The dummy values keep the tests independent from your `.env`.

## How the tests are written

- **`TestClient`** (in `test_health.py` and `test_logging.py`) calls the FastAPI app in the same process, without starting a server: `client.get("/api/health")`.
- **`monkeypatch`** (in `test_config.py`) changes environment variables for one test only and restores them afterwards.
- **`Settings(_env_file=None)`** builds the settings without reading your local `.env`, so the result does not depend on your machine.
- **`caplog`** (in `test_logging.py`) is a pytest fixture that collects the log records emitted during a test, so the test can check what was logged.
- **`LogRecord` built by hand** (in `test_logging.py`) tests the log formatter and filter directly, without going through the API.

## Side effects

The tests import the app, and importing it sets up logging, which creates the `logs/` folder in the current directory. That folder is ignored by git.

## Adding a test

Create `tests/test_<module>.py` and name each function `test_<something>`. pytest finds them by these names.

```python
def test_something() -> None:
    assert 1 + 1 == 2
```

A good test fails when the thing it protects breaks. For example, `test_query_string_is_not_logged` fails if the middleware starts logging the full URL instead of only the path.

## Before committing

```bash
make check
```

`make check` runs `make lint` (ruff, format check, and mypy) and then `make test`.

The pre-commit hook runs ruff and mypy on every commit, but it does **not** run the tests: they are slower, and the CI will run them on every push.

## Later

When the database layer arrives, its tests will need the Compose services running (see [docker.md](docker.md)) and a separate test database, so tests never touch your development data.
