# GroupUp

A FastAPI backend for managing user groups and polls. Users can register, create groups, invite members, and run polls within those groups.

## Tech Stack

- **Python 3.12+**
- **FastAPI** — async web framework
- **SQLAlchemy 2.0** — async ORM with `asyncpg` driver
- **PostgreSQL** — database
- **Alembic** — database migrations
- **PyJWT** — JWT-based authentication
- **pwdlib (Argon2)** — password hashing
- **uv** — package management

## Project Structure

```
GroupUp/
├── src/
│   ├── main.py             # App entry point, router registration
│   ├── config.py           # Global settings (loaded from .env)
│   ├── database.py         # Async engine, session factory, DB init
│   ├── models.py           # Base, User model, group_members association table
│   ├── dependencies.py     # Shared FastAPI dependencies (DB session, auth)
│   ├── exceptions.py       # Shared HTTP exceptions
│   ├── services.py         # Shared service utilities
│   ├── auth/
│   │   ├── router.py       # /auth routes: register, login, logout
│   │   ├── services.py     # User creation, authentication, token logic
│   │   ├── models.py       # RefreshToken model
│   │   ├── schemas.py      # UserCreate, UserResponse, Token schemas
│   │   ├── config.py       # Auth-specific config
│   │   ├── dependencies.py # Auth dependencies
│   │   └── exceptions.py   # Auth-specific exceptions
│   └── groups/
│       ├── router.py       # /group routes: groups, members, polls
│       ├── services.py     # Group, member, and poll business logic
│       ├── models.py       # Group, Poll, PollOption, PollResponse models
│       ├── schemas.py      # Pydantic schemas for groups and polls
│       ├── config.py       # Group-specific config
│       ├── dependencies.py # Group dependencies
│       └── exceptions.py   # Group-specific exceptions
├── migrations/             # Alembic migration scripts
├── alembic.ini             # Alembic configuration
├── pyproject.toml          # Project metadata and dependencies
├── .env                    # Environment variables (not committed)
└── .python-version         # Pinned Python version
```

## Database Models

| Model | Table | Description |
|---|---|---|
| `User` | `users` | Registered users |
| `RefreshToken` | `refresh_tokens` | JWT refresh tokens with blacklist support |
| `Group` | `groups` | User-created groups |
| `group_members` | `group_members` | Many-to-many: users ↔ groups |
| `Poll` | `polls` | Polls belonging to a group |
| `PollOption` | `poll_options` | Answer options for a poll |
| `PollResponse` | `poll_responses` | A user's vote on a poll (one vote per user per poll) |

## API Endpoints

### Auth — `/auth`

| Method | Path | Description |
|---|---|---|
| `POST` | `/auth/register` | Create a new user account |
| `POST` | `/auth/login` | Authenticate and receive access + refresh tokens |
| `POST` | `/auth/logout` | Logout (stub) |

Authentication uses JWT. The access token (15 min expiry) must be passed as an `access-token` header on protected routes.

### Groups — `/group`

| Method | Path | Description |
|---|---|---|
| `POST` | `/group/create` | Create a new group |
| `DELETE` | `/group/delete/{group_id}` | Delete a group |
| `POST` | `/group/add_member/{member_id}/group/{group_id}` | Add a member to a group |
| `POST` | `/group/remove_member/{member_id}/group/{group_id}` | Remove a member from a group |

### Polls — `/group`

| Method | Path | Description |
|---|---|---|
| `POST` | `/group/{group_id}/poll` | Create a poll in a group |
| `GET` | `/group/poll/{poll_id}` | Get a poll by ID |
| `PATCH` | `/group/poll/{poll_id}` | Update a poll's question |
| `DELETE` | `/group/poll/{poll_id}` | Delete a poll |
| `POST` | `/group/poll/{poll_id}/response` | Submit a response to a poll |
| `GET` | `/group/poll/{poll_id}/responses` | Get all responses for a poll |
| `DELETE` | `/group/poll/{poll_id}/response` | Delete your response from a poll |

## Setup

### Prerequisites

- Python 3.12+
- PostgreSQL running locally
- [`uv`](https://github.com/astral-sh/uv) installed

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd GroupUp
uv sync
```

### 2. Configure environment

Copy the example below into a `.env` file at the project root:

```env
SECRET_KEY=<your-secret-key>
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_M=15
REFRESH_TOKEN_EXPIRE_D=1

DB_USER=postgres
DB_PASS=<your-db-password>
DB_HOST=localhost
DB_NAME=groupup_db
DATABASE_URL=postgresql+asyncpg://<DB_USER>:<DB_PASS>@<DB_HOST>/<DB_NAME>
```

### 3. Create the database

```bash
psql -U postgres -c "CREATE DATABASE groupup_db;"
```

### 4. Run migrations

```bash
uv run alembic upgrade head
```

### 5. Start the server

```bash
uv run fastapi dev src/main.py
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.
