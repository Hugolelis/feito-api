# Tests

The tests use [pytest](https://pytest.org). They do not need Docker or a `.env` file.

```bash
poetry run pytest
```

## Useful options

| Goal | Command |
|---|---|
| Show each test name | `poetry run pytest -v` |
| Short output | `poetry run pytest -q` |
| Stop at the first failure | `poetry run pytest -x` |
| One file | `poetry run pytest tests/test_health.py` |
| Tests whose name contains a word | `poetry run pytest -k uptime` |

## What is covered today

| File | What it checks |
|---|---|
| `tests/test_health.py` | `GET /api/health` returns 200 with `{"status": "ok"}`, and `GET /api/health/uptime` returns 200 with a non-negative `uptime_seconds` |
| `tests/test_config.py` | The settings refuse to load when a required variable is missing (`SECRET_KEY`), and the error names the variable |

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

- **`TestClient`** (in `test_health.py`) calls the FastAPI app in the same process, without starting a server: `client.get("/api/health")`.
- **`monkeypatch`** (in `test_config.py`) changes environment variables for one test only and restores them afterwards.
- **`Settings(_env_file=None)`** builds the settings without reading your local `.env`, so the result does not depend on your machine.

## Adding a test

Create `tests/test_<module>.py` and name each function `test_<something>`. pytest finds them by these names.

```python
def test_something() -> None:
    assert 1 + 1 == 2
```

## Before committing

```bash
poetry run ruff check .
poetry run ruff format --check .
poetry run pytest
```

## Later

When the database layer arrives, its tests will need the Compose services running (see [docker.md](docker.md)) and a separate test database, so tests never touch your development data.
