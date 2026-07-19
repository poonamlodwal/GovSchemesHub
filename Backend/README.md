# SchemeHub Backend

AI-assisted platform that helps Indian citizens discover government schemes they are eligible for, built as a Flask REST API.

## Project Overview

SchemeHub lets citizens register, complete a profile, search and filter government schemes, check eligibility, receive AI-assisted recommendations, upload supporting documents, and chat with an AI assistant. Administrators can manage schemes, verify documents, send notifications, and monitor the platform through a dashboard and audit trail.

## Features

- JWT-based authentication (access + refresh tokens, role-aware claims, logout/blocklist)
- Government scheme catalog with categories, search, filtering, and pagination
- Eligibility engine and personalized scheme recommendations with a match score
- Document upload with type/size/extension validation and ownership-based access control
- AI chat module (Flask integration layer; the RAG/Gemini implementation is a separate module)
- User and admin notifications, including broadcast-to-all
- Admin dashboard with platform-wide statistics and recent activity
- Audit logging with filtering by user and action
- Health/system-info endpoints for monitoring

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Framework | Flask |
| ORM | SQLAlchemy (Flask-SQLAlchemy) |
| Database | MySQL |
| Auth | JWT (Flask-JWT-Extended) |
| Password hashing | Flask-Bcrypt |
| Migrations | Flask-Migrate |
| CORS | Flask-Cors |
| WSGI server (production) | Gunicorn |
| AI (external module) | Google Gemini |

## Folder Structure

```
SchemeHub/
├── run.py                  # Application entry point
├── requirements.txt
├── Procfile                # Render/Gunicorn start command
├── .env.example
├── .gitignore
├── app/
│   ├── __init__.py         # App factory, blueprint registration, error handlers
│   ├── config.py           # Environment-driven configuration
│   ├── extensions.py       # Flask extension instances + init/logging wiring
│   ├── base_model.py       # Shared SQLAlchemy base model (soft delete, timestamps)
│   ├── controllers/        # Request/response handling per module
│   ├── routes/             # Blueprint URL wiring
│   ├── services/           # Business logic per module
│   ├── models/             # SQLAlchemy models
│   ├── middleware/
│   ├── utils/               # Validators, response helpers, decorators, file handling
│   ├── uploads/              # Uploaded documents (local/dev; gitignored)
│   └── logs/                 # Rotating file logs (local/dev; gitignored)
├── instance/
├── migrations/
└── tests/
```

## Installation

```bash
git clone <repository-url>
cd SchemeHub
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then edit .env with real values
flask --app run db upgrade      # apply migrations
```

## Environment Variables

Copy `.env.example` to `.env` and set real values. Never commit `.env`.

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Flask session/signing secret |
| `JWT_SECRET_KEY` | JWT signing secret |
| `JWT_ACCESS_TOKEN_EXPIRES` / `JWT_REFRESH_TOKEN_EXPIRES` | Token lifetimes, in seconds |
| `DATABASE_URL` | Full DB connection string (takes priority; used by most PaaS providers including Render) |
| `SQLALCHEMY_DATABASE_URI` | Fallback DB connection string if `DATABASE_URL` isn't set |
| `UPLOAD_FOLDER` | Directory for uploaded documents |
| `MAX_CONTENT_LENGTH` | Max upload size in bytes |
| `GEMINI_API_KEY` | Google Gemini API key (used by the AI/RAG module) |
| `CORS_ORIGINS` | Comma-separated list of allowed origins |
| `LOG_LEVEL` / `LOG_FOLDER` | Logging verbosity and local log file location |
| `HOST` / `PORT` | Bind address/port for the dev server |
| `FLASK_ENV` | `development`, `production`, or `testing` |
| `FLASK_DEBUG` | `1` to enable debug mode locally |

## How to Run

**Development:**
```bash
python run.py
```

**Production (Gunicorn, as used by the included `Procfile`):**
```bash
gunicorn run:app --bind 0.0.0.0:$PORT
```

## API Categories

| Prefix | Purpose |
|---|---|
| `/api/auth` | Registration, login, refresh, current user, logout |
| `/api/schemes` | Scheme CRUD, filtering, search by category/state |
| `/api/categories` | Scheme categories |
| `/api/recommendations` | Personalized, eligibility-scored scheme recommendations |
| `/api/search` | Public advanced scheme search |
| `/api/documents` | Document upload, listing, retrieval, deletion |
| `/api/chat` | AI chat integration layer |
| `/api/notifications` | User notification inbox |
| `/api/admin/notifications` | Admin: send/broadcast/delete notifications |
| `/api/admin/dashboard` | Admin: platform statistics and recent activity |
| `/api/admin/audit` | Admin: audit log inspection |
| `/api/system` | Health check, system info, ping (monitoring) |

## Future Improvements

- Wire in the AI/RAG module (Gemini + retrieval) behind the existing `/api/chat` placeholder
- Admin authentication/login flow issuing `role: admin` tokens (currently only user login exists)
- Move the in-memory JWT blocklist to a persistent/shared store (e.g. Redis) for multi-instance deployments
- Document verification workflow (approve/reject with reviewer notes)
- Rate limiting on public endpoints (`/api/search`, `/api/auth/login`)
- Structured (JSON) logging for easier log aggregation in production
