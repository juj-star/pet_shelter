from flask import Flask
from werkzeug.security import generate_password_hash
from .database.db import init_db
from .database.db_utils import find_user_by_username, insert_hooman  # make sure these functions exist
import os

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your_secret_key_here'

    # Get MongoDB URI from environment variables
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/pet_shelter')
    app.config["MONGO_URI"] = mongo_uri

    # Initialize MongoDB
    init_db(app)

    # Register Blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Function to create an admin user
    def create_admin_user():
        admin_username = 'admin'
        admin_email = 'admin@example.com'
        # Hardcoded password for non-production use
        admin_password = 'admin'  # Change this to your desired password

        # Check if the admin user already exists
        existing_admin = find_user_by_username(admin_username)
        if not existing_admin:
            hashed_password = generate_password_hash(admin_password)
            admin_data = {
                'username': admin_username,
                'email': admin_email,
                'password': hashed_password,
                # Add any other fields required for the admin user
                'is_admin': True  # Make sure to have a flag for admin users
            }
            # Insert admin into database
            insert_hooman(admin_data)
            print('Admin user created')
        else:
            print('Admin user already exists')

    # Run the create_admin_user function before the first request
    with app.app_context():
        create_admin_user()

    return app
