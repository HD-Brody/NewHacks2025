## NewHacks2025 — Copilot / AI agent instructions

Purpose: give a focused, actionable summary so an AI coding agent can be productive immediately in this repo.

- Big picture
  - Monorepo-style skeleton with two parts:
    - backend/ — Flask app. A small factory in `backend/app/__init__.py` (`create_app`) registers a blueprint at url_prefix `/api`.
      - Example route: `backend/app/routes.py` defines Blueprint `bp` and `/hello` which becomes `/api/hello`.
      - Entrypoint: `backend/run.py` runs the dev server on 127.0.0.1:5000 (debug mode). Use a WSGI server for prod.
    - frontend/ — Vite + React + Tailwind. React app lives in `frontend/src`, main entry `frontend/src/main.jsx` and `frontend/src/App.jsx`.
      - The client calls backend with relative URLs (example: `fetch('/api/hello')` in `App.jsx`). The Vite dev server proxies `/api` to the backend (see README).

- Primary integration points
  - API prefix: all backend routes are mounted under `/api` (see `create_app()` registration).
  - Frontend uses relative `/api/*` paths — keep this contract when changing ports or adding hosts.
  - Ports used by convention in this repo: backend 5000, Vite dev usually 5173. The README documents the standard dev flow.

- How to run (developer workflows) — PowerShell (project README contains same commands)
  - Backend (create venv, install, run):
    - python -m venv .venv
    - .\.venv\Scripts\Activate.ps1
    - pip install -r backend\requirements.txt
    - python backend\run.py
  - Frontend:
    - cd frontend
    - npm install
    - npm run dev
  - Order: start backend first, then frontend. Open Vite URL (http://localhost:5173 by default).

- Code/Editing conventions specific to this repo
  - Add backend endpoints by editing `backend/app/routes.py` or add new blueprints and register them in `create_app()`.
  - Keep the API prefix `/api` stable — frontend assumes it.
  - No CORS or auth currently configured. If adding cross-origin support for non-dev scenarios, add and configure `flask-cors` explicitly.
  - Environment files: `python-dotenv` is listed in `backend/requirements.txt`; expect `.env` usage for secret/config values.

- Files to inspect when changing behavior
  - backend/app/__init__.py — app factory and blueprint registration
  - backend/app/routes.py — current API examples (hello route)
  - backend/run.py — dev server launch (debug=True)
  - backend/requirements.txt — Python deps
  - frontend/package.json — scripts and deps
  - frontend/src/App.jsx — example API call and UI component

- Editing examples (explicit)
  - To add GET /api/status: add
    - new route function to `backend/app/routes.py` (or new module), then restart backend.
  - To update client to call a new endpoint: edit `frontend/src/App.jsx` and use `fetch('/api/your-route')`.

- Tests / CI
  - No automated tests or CI config are present in the repo; adding tests should follow lightweight patterns: pytest for Flask, and React testing-library for frontend (optional).

- Notes and limitations discovered (so AI agents avoid incorrect changes)
  - This is a minimal skeleton — do not assume production-ready settings (no CORS, no auth, debug True, no Dockerfile).
  - Keep changes small and well-scoped: the README documents the expected dev workflow; mirror or update README when you change commands/ports.

If anything here is unclear or you want more detail (CI, Docker, auth, or example tests), tell me which area to expand and I will update this file.
