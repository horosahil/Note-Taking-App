Note Taking App

- Frontend: Next.js 14 (App Router) + Zustand + React Query (Axios) + Tailwind (no UI component libs; hand-crafted components). Optional Framer Motion used for simple animations.

- Backend: FastAPI + MongoDB (Motor) with JWT auth via HttpOnly cookie. Clean structure, CRUD for notes, user auth, CORS, and a health endpoint.

- Docker: docker-compose spins up MongoDB, backend, and frontend.

- SEO: title/description/OG/keywords via Next’s metadata.

- Rich text: lightweight contentEditable editor (no external editor library).

- Perf test: example k6 script (Docker-run) for login & note flow.
