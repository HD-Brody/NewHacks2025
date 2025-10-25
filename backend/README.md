# Backend — dependencies & setup

This folder contains the Flask backend for the project.

Dependencies (see `requirements.txt`):
- Flask >= 2.0
- python-dotenv
- Flask-Cors (for cross-origin resource sharing in development)

Quick setup (PowerShell):

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Notes:
- The dev server binds to `127.0.0.1:5000` by default.
- Use a `.env` file with `python-dotenv` for environment variables in development.
 - The app enables CORS in development using `Flask-Cors` (see `app/__init__.py`).
