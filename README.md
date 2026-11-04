# Feito

<div align="left">

[![License](https://img.shields.io/badge/License-MIT-1a1a2e?style=for-the-badge&logoColor=white)](LICENSE)
[![Python](https://img.shields.io/badge/Python-%3E%3D3.11-1a1a2e?style=for-the-badge&logo=python&logoColor=white)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-1a1a2e?style=for-the-badge&logo=fastapi&logoColor=white)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-1a1a2e?style=for-the-badge&logo=postgresql&logoColor=white)]()
[![React](https://img.shields.io/badge/React-Vite-1a1a2e?style=for-the-badge&logo=react&logoColor=white)]()
[![Status](https://img.shields.io/badge/Status-In_Development-1a1a2e?style=for-the-badge&logoColor=white)]()

</div>

> **Feito** is a full-stack to-do list application with email-confirmed accounts, Google sign-in, custom lists, smart views, and a monthly calendar. Built as a monorepo with FastAPI and React, in Portuguese and English.

<details>
<summary><strong>Table of Contents</strong></summary>

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture & Design Decisions](#architecture--design-decisions)
- [Getting Started](#getting-started)
- [License](#license)
- [Author](#author)

</details>

---

## About

Feito is a study project built end to end, from the database to the interface, with the goal of practicing a real-world stack: secure authentication, a typed REST API, automated tests, and a responsive React front end.

> The project is under active development. This README describes the planned scope and will be filled in as each part is built.

---

## Features

| Capability | Description |
|---|---|
| **Authentication** | Email and password sign-up with email confirmation, plus Google OAuth 2.0 (state and PKCE) |
| **Sessions** | Short-lived JWT access token with a refresh token in an `httpOnly` cookie |
| **Lists** | Custom lists, with default lists created for every new account |
| **Tasks** | Create, edit, complete, and favorite tasks |
| **Smart Views** | Filtered views such as important and completed tasks, with sidebar counters |
| **Calendar** | Monthly calendar highlighting the days that have tasks |
| **Profile** | Edit profile, change password, and delete account |
| **i18n** | Interface available in Portuguese and English |

---

## Tech Stack

| Tool | Purpose |
|---|---|
| [Python](https://python.org) | Back end language |
| [FastAPI](https://fastapi.tiangolo.com) | REST API framework |
| [PostgreSQL](https://postgresql.org) | Database |
| [SQLAlchemy 2](https://www.sqlalchemy.org) | ORM |
| [Alembic](https://alembic.sqlalchemy.org) | Database migrations |
| [React](https://react.dev) | Front end library |
| [Vite](https://vite.dev) | Front end build tool |
| [TypeScript](https://www.typescriptlang.org) | Front end language |
| [Docker Compose](https://docs.docker.com/compose/) | Local PostgreSQL and Mailpit |

---

## Architecture & Design Decisions

```
Feito-product/
├── api/                    # FastAPI back end
├── web/                    # React + Vite + TypeScript front end
├── .editorconfig
├── .gitignore
├── LICENSE
└── README.md
```

- **Monorepo:** `api/` and `web/` live in the same repository, so a change that touches both ships in a single commit.
- **Sessions:** a short-lived JWT access token plus a refresh token stored in an `httpOnly` cookie, which keeps the refresh token out of reach of JavaScript.
- **Password hashing:** Argon2.
- **Email:** SMTP, with Mailpit as the local inbox during development.
- **Local environment:** PostgreSQL and Mailpit run through Docker Compose.

---

## Getting Started

> Setup instructions will be added as the API and the web app are built.

```bash
# Clone the repository
git clone https://github.com/Hugolelis/Feito-product.git
cd Feito-product
```

---

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.

---

## Author

[Hugolelis](https://github.com/Hugolelis)
