# Carpool Connect

A student-level carpool management project with a backend API and a simple frontend dashboard.

## What it does

This app lets users:
- register and log in with JWT auth
- browse carpool rides
- join rides as a participant
- view their own bookings
- submit and read reviews

It also includes:
- a landing page at `/`
- a basic dashboard at `/dashboard.html`
- Docker Compose support for local setup

## Project features

- Express backend with clean routes
- MySQL connection using `mysql2/promise`
- JWT authentication and password hashing
- Basic frontend landing page and dashboard
- Containerized dev environment
- Simple, student-friendly code structure

## Setup

1. Install dependencies:

   ```bash
   npm install
   ```

2. Start the database and app with Docker Compose:

   ```bash
   docker compose up --build
   ```

3. Open the site in your browser:

   ```text
   https://<your-github-codespace-host>-5000.app.github.dev/
   ```

4. Open the dashboard:

   ```text
   https://<your-github-codespace-host>-5000.app.github.dev/dashboard.html
   ```

## Quick start

- `GET /` — landing page
- `GET /health` — API health check
- `GET /api/rides` — list rides
- `POST /api/auth/login` — log in
- `POST /api/auth/register` — register new user

## Frontend pages

- `/` — landing page with project overview
- `/dashboard.html` — simple frontend dashboard for login and API examples

## Usage examples

Login with curl:

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username": "student1", "password": "secret123"}'
```

View rides:

```bash
curl http://localhost:5000/api/rides
```

Health check:

```bash
curl http://localhost:5000/health
```

## Notes

- This is intentionally a student-level capstone project.
- Use the dashboard as a simple demo interface, not a full production frontend.
- Keep `.env` secret and do not commit it.
