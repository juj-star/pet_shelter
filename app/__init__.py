from flask import Flask
from werkzeug.security import generate_password_hash
from .database.db import init_db  # Ensure that mongo is imported here
from .database.db_utils import find_user_by_username, insert_hooman
import os

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your_secret_key_here'
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/pet_shelter')
    app.config["MONGO_URI"] = mongo_uri

    # Initialize MongoDB
    init_db(app)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    def create_admin_user():
        admin_username = 'admin'
        admin_email = 'admin@example.com'
        admin_password = 'admin_password'  # Replace with a secure password in production

        # Check if the admin user already exists
        existing_admin = find_user_by_username(admin_username)
        if not existing_admin:
            hashed_password = generate_password_hash(admin_password)
            admin_data = {
                'username': admin_username,
                'email': admin_email,
                'password': hashed_password,
                'is_admin': True  # This is the attribute that grants admin rights
            }
            # Insert the admin user into the database
            insert_hooman(admin_data)
            print('Admin user created')
        else:
            print('Admin user already exists')

    with app.app_context():
        create_admin_user()

    return app
