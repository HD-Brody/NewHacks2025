from flask import Flask
from dotenv import load_dotenv
import os
import google.generativeai as genai

# --- Load environment variables ---
load_dotenv()

# --- Configure Gemini API ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

genai.configure(api_key=GEMINI_API_KEY)
GEMINI_MODEL = "gemini-2.5-flash"  # ✅ your verified working model
from flask_cors import CORS
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)

    # Store Gemini configuration in app.config so all routes can access it
    app.config["GEMINI_API_KEY"] = GEMINI_API_KEY
    app.config["GEMINI_MODEL"] = GEMINI_MODEL
    app.config["GEMINI_CLIENT"] = genai

    # --- Register Blueprints ---
    from .routes import bp
    from .itinerary_routes import itinerary_bp
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.register_blueprint(bp, url_prefix='/api')
    app.register_blueprint(itinerary_bp, url_prefix='/api')
    
    @app.route('/')
    def home():
        return {'message': 'Flask backend is running'}
    return app
