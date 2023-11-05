from flask import Flask
from werkzeug.security import generate_password_hash
from .database.db import init_db
from .database.db_utils import find_user_by_username, insert_hooman  # make sure these functions exist
import os
from .models.hooman import Hooman

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
        admin_password = 'admin'  # Replace with a secure password in production

        # Check if the admin user already exists
        existing_admin = find_user_by_username(admin_username)
        if not existing_admin:
            hashed_password = generate_password_hash(admin_password)
            # Instantiate the Hooman object with admin attributes
            admin_hooman = Hooman(
                hooman_id=None,
                name='Admin',  # You can give a name to the admin
                email=admin_email,
                phone='0000000000',  # Since it's required by Hooman, provide a dummy or actual phone number
                address='Admin Address',  # Provide a dummy or actual address
                is_admin=True,  # Set the is_admin attribute to True
                adoption_history=[]  # Admin's adoption history is empty initially
            )
            # Use the to_document method to convert the Hooman object to a dictionary suitable for insertion
            admin_data = admin_hooman.to_document()
            admin_data['username'] = admin_username  # Add the username to the document
            admin_data['password'] = hashed_password  # Include the hashed password in the document

            # Insert the admin user into the database
            insert_hooman(admin_data)
            print('Admin user created')
        else:
            print('Admin user already exists')

    # Run the create_admin_user function before the first request
    with app.app_context():
        create_admin_user()

    return app