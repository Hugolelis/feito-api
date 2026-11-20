# Docker and local environment

Docker Compose runs the two services the API needs during development. The API itself runs on your machine with `uvicorn`, not in Docker.

| Service | Container | Image | What it is for | Address |
|---|---|---|---|---|
| `db` | `feito-db` | `postgres:16` | PostgreSQL database | `localhost:5433` |
| `mailpit` | `feito-mailpit` | `axllent/mailpit` | Fake inbox that catches the confirmation emails | SMTP `localhost:1025`, web UI http://localhost:8025 |

All ports are bound to `127.0.0.1`, so only your own machine can reach them.

## Before the first run

The database password is not stored in the compose file. It comes from your `.env`:

```bash
cp .env.example .env
```

Then set `POSTGRES_PASSWORD` and use the same password in `DATABASE_URL`. A random one:

```bash
python3 -c "import secrets; print(secrets.token_hex(24))"
```

```
POSTGRES_PASSWORD=<generated password>
DATABASE_URL=postgresql+psycopg://feito:<generated password>@localhost:5433/feito
```

The user and the database name (`feito`) are created by the compose file (`POSTGRES_USER` and `POSTGRES_DB`). The `DATABASE_URL` only uses them, so both must match.

## Commands

The compose file lives in `docker/`, so every command needs `--env-file .env -f docker/compose.yaml`. Two of them have shortcuts: `make up` and `make down`.

| Goal | Command |
|---|---|
| Start in the background | `docker compose --env-file .env -f docker/compose.yaml up -d` |
| See what is running | `docker compose --env-file .env -f docker/compose.yaml ps` |
| Read the logs of a service | `docker compose --env-file .env -f docker/compose.yaml logs db` |
| Stop, keep the data | `docker compose --env-file .env -f docker/compose.yaml down` |
| Stop and erase the data | `docker compose --env-file .env -f docker/compose.yaml down -v` |

Compose commands use the **service** name (`db`, `mailpit`). Plain Docker commands use the **container** name (`feito-db`, `feito-mailpit`).

## Check that it works

1. `ps` shows `db` and `mailpit` as running.
2. http://localhost:8025 opens the Mailpit inbox.
3. The API can reach the database with the password from your `.env`:

```bash
poetry run python -c "import psycopg; from app.core.config import settings; psycopg.connect(settings.database_url.replace('+psycopg', '')).close(); print('connected')"
```

It prints `connected`. The `.replace` is needed because `postgresql+psycopg://` is SQLAlchemy notation, while `psycopg` alone expects `postgresql://`.

## Data

The database files live in the named volume `pgdata`, outside the container. Recreating the container keeps your data. `down -v` removes the volume and gives you an empty database on the next `up`.

PostgreSQL only reads `POSTGRES_USER`, `POSTGRES_PASSWORD` and `POSTGRES_DB` when it creates a new volume. If you change them later, run `down -v` first, or the existing database keeps the old values.

## Which host the API uses

| Where the API runs | Host and port in `DATABASE_URL` |
|---|---|
| On your machine (today) | `localhost:5433`, the published port |
| In a container of the same compose (deploy) | `db:5432`, the service name and the internal port |

## Troubleshooting

- **`db` exits right after starting.** Run `logs db`. If `POSTGRES_PASSWORD` is missing or empty in `.env`, PostgreSQL refuses to start.
- **Port already in use.** Another PostgreSQL may already use the port. The compose file publishes `5433` instead of the default `5432` for this reason. Change the left number in `ports` and in `DATABASE_URL` if `5433` is also taken.
- **`password authentication failed`.** The volume was created with another password. Run `down -v` and `up -d` again. This erases the data.
- **The API port is busy.** `make run` uses port 8001 (the default 8000 is often used by other tools). Use another one with `make run PORT=8002`.
