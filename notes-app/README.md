# Notes App (Next.js + FastAPI + MongoDB)

> ⚠️ Assignment note: If your rules forbid AI-generated code, **do not submit this as-is**. Use it for learning only and attribute any copied snippets in your README.

## Stack
- **Frontend**: Next.js 14 App Router, Tailwind CSS, Zustand, React Query, Axios, Framer Motion (optional flair)
- **Backend**: FastAPI (Python), MongoDB (Motor), JWT auth with HttpOnly cookies
- **Docker**: `docker-compose` for front, back, and MongoDB

## Run locally (Docker)
1. Copy `.env.example` to `.env` and adjust values.
2. Build & start:
   ```bash
   docker compose --env-file .env up --build
   ```
3. Frontend: http://localhost:3000  
   Backend: http://localhost:8000/docs

## Features
- Sign up / Sign in / Logout (JWT set as HttpOnly cookie)
- Create / View / Edit / Delete notes
- Simple rich text editor using `contentEditable` (no external UI libs)
- Basic SEO via Next metadata
- Code splitting & client-side caching via React Query

## Backend Endpoints (summary)
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/me`
- `GET /api/notes/`
- `POST /api/notes/`
- `GET /api/notes/{note_id}`
- `PUT /api/notes/{note_id}`
- `DELETE /api/notes/{note_id}`

## Performance Testing (example via k6 Docker)
You can run k6 against the backend without new dependencies in the codebase:
```bash
docker run --rm -i grafana/k6 run - < ./perf/login-and-list.js
```
See `perf/login-and-list.js` for a simple scenario.

## Design decisions & trade-offs
- **MongoDB** chosen for flexible document storage and rapid prototyping.
- **JWT in HttpOnly cookie** for improved XSS resilience while keeping SPA ergonomics.
- **No UI libs**; all components styled with Tailwind utilities.
- **contentEditable** used to avoid pulling a rich-text dependency.