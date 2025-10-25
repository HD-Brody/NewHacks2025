from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)

    # Register API blueprints
    from .routes import bp
    from .itinerary_routes import itinerary_bp
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.register_blueprint(bp, url_prefix='/api')
    app.register_blueprint(itinerary_bp, url_prefix='/api')
    
    @app.route('/')
    def home():
        return {'message': 'Flask backend is running'}
    return app
