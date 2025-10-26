from flask import Flask
from dotenv import load_dotenv
import os
import logging

# Optional import for Google Generative AI (Gemini). If unavailable, LLM features
# will be disabled but the rest of the app should still run.
try:
    import google.generativeai as genai
except Exception:
    genai = None
    logging.getLogger(__name__).warning("google.generativeai not installed; LLM features disabled.")

# --- Load environment variables ---
load_dotenv()

# --- Configure Gemini API only if client is available and key present ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# model can be overridden in env; default is kept
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if genai is not None:
    if GEMINI_API_KEY:
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            logging.getLogger(__name__).info("Configured google.generativeai client.")
        except Exception:
            # If configuration fails, disable genai to avoid crashing the app.
            logging.getLogger(__name__).exception("Failed to configure google.generativeai; disabling LLM features.")
            genai = None
    else:
        logging.getLogger(__name__).warning("GEMINI_API_KEY not set; LLM features disabled.")

from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    # Store Gemini configuration in app.config so routes can detect availability
    app.config["GEMINI_API_KEY"] = GEMINI_API_KEY
    app.config["GEMINI_MODEL"] = GEMINI_MODEL
    app.config["GEMINI_CLIENT"] = genai

    # --- Register Blueprints ---
    from .routes import bp
    from .itinerary_routes import itinerary_bp

    frontend_origin = os.environ.get("FRONTEND_URL")
    if frontend_origin:
        CORS(app, resources={r"/api/*": {"origins": frontend_origin}})
    else:
        # dev fallback: allow all (only in development)
        CORS(app)

    app.register_blueprint(bp, url_prefix='/api')
    app.register_blueprint(itinerary_bp, url_prefix='/api')

    @app.route('/')
    def home():
        return {'message': 'Flask backend is running'}

    return app
