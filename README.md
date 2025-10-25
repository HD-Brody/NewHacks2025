# NewHacks2025 - React + Tailwind (Vite) frontend and Flask backend skeleton

This repository contains a minimal skeleton for a React frontend (Vite + Tailwind) and a small Flask backend.

## What’s included

- `frontend/`: Vite + React + Tailwind CSS (client-side app)
- `backend/`: Flask app (API mounted at `/api`)

---

## Dependencies (summary)

Backend (Python)
- See `backend/requirements.txt` — this project depends on:
	- Flask >= 2.0
	- python-dotenv

Frontend (Node)
- See `frontend/package.json` — notable dependencies included:
	- react ^18.2.0
	- react-dom ^18.2.0
	- leaflet ^1.9.x
	- react-leaflet ^4.x
	- mapbox-gl ^3.x
	- Tailwind / Vite dev tooling in `devDependencies`

If you add or change dependencies, update the files above (requirements.txt and package.json) and re-run the install steps below.

---

## Setup (PowerShell)

1) Backend (Python)

```powershell
# from repo root
cd backend
# create a virtual environment (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# install python deps listed in backend/requirements.txt
pip install -r requirements.txt
# run the Flask backend (development)
python run.py
```

Notes:
- `python-dotenv` is included so you can place environment variables in a `.env` file if needed.
- The dev server in `backend/run.py` binds to `127.0.0.1:5000` by default (see file).

2) Frontend (Node)

```powershell
cd frontend
# install node dependencies
npm install
# run the Vite dev server
npm run dev
```

Notes:
- The project uses Vite; the dev server typically starts on http://localhost:5173.
- The frontend is configured to call the backend using relative `/api/*` paths; the Vite dev server is expected to proxy `/api` requests to the Flask backend during development.

---

## Quick test

1. Start the backend first (so `/api` is available): run the backend steps above.
2. Start the frontend dev server.
3. Open the Vite URL (usually http://localhost:5173) and exercise the app. The frontend will call `/api/hello` as a basic smoke test.

---

## Helpful tips

- If you add Leaflet/Mapbox dependencies, ensure their CSS is imported in the React components (for Leaflet: `import 'leaflet/dist/leaflet.css'`).
- If you encounter peer-dependency errors when installing frontend packages, try `npm install --legacy-peer-deps` (not recommended for long-term — prefer matching versions).
- For production, consider building the frontend (`npm run build`) and serving the static files from a proper web server; add Docker or CI as needed.

If you want, I can also add a short section with the exact install commands for common shells (PowerShell, bash) or create a tiny `dev-setup.md` with troubleshooting steps.
