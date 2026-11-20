<img src="docs/FeitoLogo.png" alt="Feito API" width="260">

# Feito

<div align="left">

[![Status](https://img.shields.io/badge/Status-In_Development-a16207?style=for-the-badge&labelColor=1a1a1a&logoColor=white)]()
[![Version](https://img.shields.io/badge/Version-0.1.0-0f766e?style=for-the-badge&labelColor=1a1a1a&logoColor=white)]()
[![License](https://img.shields.io/badge/License-MIT-0f766e?style=for-the-badge&labelColor=1a1a1a&logoColor=white)](LICENSE)

</div>

> **Feito** is a to-do list REST API with email-confirmed accounts, Google sign-in, custom lists, smart views, and a monthly calendar endpoint. Built with FastAPI, with Portuguese and English emails.

<details>
<summary><strong>Table of Contents</strong></summary>

- [About](#about)
- [Features](#features)
- [Usage Flow](#usage-flow)
- [Tech Stack](#tech-stack)
- [Architecture & Design Decisions](#architecture--design-decisions)
- [Getting Started](#getting-started)
- [Author](#author)
- [License](#license)

</details>

---

## About

Feito is a study project built as an API only, from the database to the HTTP layer, with the goal of practicing a real-world stack: secure authentication, a typed REST API, and automated tests. A web front end may be added later.

> The project is in its very first stage. The repository holds only the Poetry setup (dependencies and a bare FastAPI app). Everything below describes the **planned scope**. This README will be updated as each part is built.

---

## Features

Planned, none of these is implemented yet.

| Capability | Description |
|---|---|
| **Authentication** | Email and password sign-up with email confirmation, plus Google OAuth 2.0 (state and PKCE) |
| **Sessions** | Short-lived JWT access token and a rotating refresh token, both returned in the JSON body |
| **Lists** | Custom lists, with default lists created for every new account |
| **Tasks** | Create, edit, complete, and favorite tasks |
| **Smart Views** | Filtered views such as important and completed tasks, with counters |
| **Calendar** | Monthly calendar highlighting the days that have tasks |
| **Profile** | Edit profile, change password, and delete account |
| **i18n** | Confirmation emails in Portuguese and English |

---

## Usage Flow

From the first sign-in, with Google or email and password, to completing the day's tasks.

![Usage flow of Feito](docs/FeitoUsageFlow.png)

> There is no front end: the client is a browser or the interactive docs at `/docs`, and the API answers with JSON.

1. **Sign-in:** the user chooses Google or email and password.
2. **Confirmation:** with email and password, the server creates a pending account and emails a confirmation link that points to the API; opening it activates the account. With Google the email arrives already verified, so this step is skipped.
3. **Session and tasks:** after signing in, the server returns an access token and a refresh token, and every change to a task is saved through the API.
4. **Exit:** the user reviews the day and signs out, which ends the session.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| [Python](https://python.org) | Back end language (3.12) |
| [Poetry](https://python-poetry.org) | Back end dependency management |
| [FastAPI](https://fastapi.tiangolo.com) | REST API framework |
| [PostgreSQL](https://postgresql.org) | Database |
| [SQLAlchemy 2](https://www.sqlalchemy.org) | ORM |
| [Alembic](https://alembic.sqlalchemy.org) | Database migrations |
| [Authlib](https://authlib.org) | Google OAuth 2.0 |
| [Pytest](https://pytest.org), [Ruff](https://docs.astral.sh/ruff/), [mypy](https://mypy-lang.org) | Tests, linting, and type checking |
| [Docker Compose](https://docs.docker.com/compose/) | Local PostgreSQL and Mailpit |

---

## Architecture & Design Decisions

```
feito-product/
├── app/                    # FastAPI application
│   ├── main.py             # Entry point
│   ├── core/               # Settings (.env) and security
│   ├── db/                 # Engine, session, and base model
│   ├── modules/            # One folder per feature (auth, users, lists, tasks, health)
│   └── utils/              # Shared helpers (email, helpers, log)
├── tests/                  # Automated tests
├── docker/                 # Docker Compose (PostgreSQL and Mailpit)
├── ci/                     # Pre-commit configuration
├── docs/                   # Guides, usage flow, and logo
├── Makefile                # Shortcuts (run, lint, test, ...)
├── pyproject.toml          # Poetry project, dependencies, and tool settings
├── .env.example            # Environment variables template
├── .gitignore
├── LICENSE
└── README.md
```

The decisions below guide the stack. Some are already in the code, and the rest arrive as each feature is built:

- **API only for now:** the code lives at the repository root, so a front end can be added later in a separate `web/` folder.
- **Feature-based layout:** each feature owns its router, models, schemas, and service inside `app/modules/`, while shared code lives in `core/`, `db/`, and `utils/`.
- **Sessions:** a short-lived JWT access token plus a rotating refresh token, both returned in the JSON body; the access token is sent in the `Authorization` header. Cookies and CORS only matter once a browser front end exists.
- **Password hashing:** Argon2.
- **Email:** SMTP, with Mailpit as the local inbox during development.
- **Local environment:** PostgreSQL and Mailpit run through Docker Compose.

---

## Getting Started

The API skeleton, the health routes, the local environment (PostgreSQL and Mailpit), and the quality tooling (ruff, mypy, pre-commit) can be run so far.

**Requirements:** Python 3.12, [Poetry](https://python-poetry.org), [Docker](https://docs.docker.com/get-docker/) with Compose, and `make` (preinstalled on most Linux and macOS systems).

```bash
# Clone the repository
git clone https://github.com/Hugolelis/feito-product.git
cd feito-product

# Install dependencies (creates .venv)
poetry install

# Create your .env from the template
cp .env.example .env

# Generate the secrets and write them into .env (nothing is printed)
SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))")
PASS=$(python3 -c "import secrets; print(secrets.token_hex(24))")
sed -i "s|^SECRET_KEY=.*|SECRET_KEY=$SECRET|" .env
sed -i "s|^POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD=$PASS|" .env
sed -i "s|^DATABASE_URL=.*|DATABASE_URL=postgresql+psycopg://feito:$PASS@localhost:5433/feito|" .env

# Install the git hook (runs ruff and mypy before each commit)
make hooks

# Start PostgreSQL and Mailpit
make up

# Run the API
make run
```

On macOS, use `sed -i ''` instead of `sed -i`.

The API runs at `http://localhost:8001`, with interactive docs at `/docs`. The Mailpit inbox is at `http://localhost:8025`. To use another port: `make run PORT=8002`.

The git hook is stored inside `.git`, so it is not part of the repository: run `make hooks` once in every clone.

### Shortcuts

| Command | What it does |
|---|---|
| `make run` | Starts the API with auto-reload (port 8001) |
| `make lint` | Checks the code without changing it: `ruff check`, `ruff format --check`, and `mypy` |
| `make format` | Fixes what ruff can fix and formats the code |
| `make test` | Runs the tests |
| `make check` | Runs `lint` and then `test` |
| `make hooks` | Installs the pre-commit hook |
| `make up` / `make down` | Starts / stops PostgreSQL and Mailpit |

More details:

- [Docker and local environment](docs/docker.md)
- [Tests](docs/testing.md)

---

## Author

[Hugolelis](https://github.com/Hugolelis)

---

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.
