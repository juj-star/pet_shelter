from flask import Flask
from .database.db import init_db
import os

def create_app():
    app = Flask(__name__)

    # Get MongoDB URI from environment variables
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/pet_shelter')
    app.config["MONGO_URI"] = mongo_uri

    # Initialize MongoDB
    init_db(app)

    # Register Blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
