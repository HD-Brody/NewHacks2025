from flask import Flask


def create_app():
    app = Flask(__name__)

    # Existing simple API routes
    from .routes import bp
    app.register_blueprint(bp, url_prefix='/api')

    # Itinerary API (placeholder)
    # Importing the module ensures the blueprint object is available here
    from .itinerary_routes import itinerary_bp
    app.register_blueprint(itinerary_bp, url_prefix='/api')

    return app
