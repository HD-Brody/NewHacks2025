# NewHacks2025 - React + Tailwind (Vite) frontend and Flask backend skeleton

This repository contains a minimal skeleton for a React frontend (Vite + Tailwind) and a Flask backend.

## What’s included

- frontend/: Vite + React + Tailwind CSS
- backend/: Flask app with a single `/api/hello` endpoint

## Setup (PowerShell)

1) Backend (Python)

```powershell
# create virtual env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
# run the Flask backend
python backend\run.py
```

2) Frontend (Node)

```powershell
cd frontend
# install deps (npm or pnpm/yarn)
npm install
# start dev server (Vite)
npm run dev
```

The frontend dev server proxies `/api` to the backend (http://127.0.0.1:5000) by default.

## Quick test

- Start the backend, then the frontend, then open the Vite dev URL (usually http://localhost:5173) and the app will call `/api/hello`.

## Next steps

- Add environment config, Dockerfile, tests, CI, and expand API/frontend.
