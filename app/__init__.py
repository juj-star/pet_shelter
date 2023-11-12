from flask import Flask
from werkzeug.security import generate_password_hash
from .database.db import init_db
from .database.db_utils import *
import os
from .models.hooman import Hooman
from .models.animal import AnimalProfile
import base64
from bson import binary
from datetime import datetime, timedelta
import random

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

    # Helper function to generate random dates within the past two months
    def generate_random_date(species):
        today = datetime.today()
        random_days = random.randint(0, 60)
        random_date = today - timedelta(days=random_days)
        return random_date.strftime('%Y-%m-%dT%H:%M:%S.%f')

    # Generate a shared random date for cats and dogs
    dog_shared_date1 = generate_random_date('cat')
    dog_shared_date2 = generate_random_date('dog')
    dog_shared_date3 = generate_random_date('dog')
    dog_shared_date4 = generate_random_date('dog')
    dog_shared_date5 = generate_random_date('dog')

    def create_animal_profiles():
        # Define a list of animal data to create profiles for
        animals_data = [
            {'type_name': 'Cat', 'breed_name': 'Abyssinian', 'dispositions': ['Good with other animals', 'Good with children'], 'pic': 'app/images/cats/abyssinian.webp', 'availability': 'Available', 'description': 'A highly active, playful, and curious cat that loves to explore.', 'date_created': dog_shared_date1},
            {'type_name': 'Cat', 'breed_name': 'Bengal', 'dispositions': ['Good with other animals', 'Good with children'], 'pic': 'app/images/cats/bengal.webp', 'availability': 'Available', 'description': 'A majestic cat that resembles a wild leopard and enjoys interactive play.', 'date_created': dog_shared_date2},
            {'type_name': 'Cat', 'breed_name': 'British Shorthair', 'dispositions': ['Good with children', 'Good with other animals'], 'pic': 'app/images/cats/british-shorthair.webp', 'availability': 'Available', 'description': 'A calm and easygoing companion, perfect for curling up on a lap.', 'date_created': dog_shared_date3},
            {'type_name': 'Cat', 'breed_name': 'Exotic Shorthair', 'dispositions': ['Good with other animals', 'Good with children'], 'pic': 'app/images/cats/exotic-shorthair.webp', 'availability': 'Available', 'description': 'An adorable cat with a sweet personality, loves to play gently.', 'date_created': dog_shared_date1},
            {'type_name': 'Cat', 'breed_name': 'Oriental Shorthair', 'dispositions': ['Good with children', 'Good with other animals'], 'pic': 'app/images/cats/oriental-shorthair.webp', 'availability': 'Available', 'description': 'A sleek, vocal cat who enjoys social interaction and play.', 'date_created': dog_shared_date4},
            {'type_name': 'Cat', 'breed_name': 'Ragdoll', 'dispositions': ['Good with other animals', 'Good with children'], 'pic': 'app/images/cats/ragdoll.webp', 'availability': 'Available', 'description': 'A large, calm cat, known for going limp like a ragdoll when held.', 'date_created': dog_shared_date5},
            {'type_name': 'Cat', 'breed_name': 'Russian Blue', 'dispositions': ['Good with other animals', 'Good with children'], 'pic': 'app/images/cats/russian-blue.webp', 'availability': 'Available', 'description': 'A reserved and gentle cat with a striking blue coat.', 'date_created': dog_shared_date3},
            {'type_name': 'Cat', 'breed_name': 'Siamese', 'dispositions': ['Good with other animals', 'Good with children'], 'pic': 'app/images/cats/siamese.webp', 'availability': 'Available', 'description': 'An outgoing and vocal breed with striking features and loyalty.', 'date_created': dog_shared_date5},
            {'type_name': 'Dog', 'breed_name': 'Coonhound', 'dispositions': ['Good with children', 'Good with other animals'], 'pic': 'app/images/dogs/coonhound.jpeg', 'availability': 'Available', 'description': 'A scent hound that is well-known for its ability to trail and tree raccoons.', 'date_created': dog_shared_date2},
            {'type_name': 'Dog', 'breed_name': 'Cardigan Welsh Corgi', 'dispositions': ['Good with children'], 'pic': 'app/images/dogs/corgi-cardigan.jpeg', 'availability': 'Available', 'description': 'A small herding dog that is both companionable and watchful.', 'date_created': dog_shared_date4},
            {'type_name': 'Dog', 'breed_name': 'Dalmatian', 'dispositions': ['Animal must be leashed at all times', 'Good with children', 'Good with other animals'], 'pic': 'app/images/dogs/dalmatian.jpeg', 'availability': 'Available', 'description': 'A distinctively spotted dog known for its energy and intelligence.', 'date_created': dog_shared_date4},
            {'type_name': 'Dog', 'breed_name': 'Pitbull', 'dispositions': ['Animal must be leashed at all times'], 'pic': 'app/images/dogs/pitbull.jpeg', 'availability': 'Available', 'description': 'A dog with a strong desire to please and a big heart.', 'date_created': dog_shared_date5},
            {'type_name': 'Dog', 'breed_name': 'Chesapeake Bay Retriever', 'dispositions': ['Good with children'], 'pic': 'app/images/dogs/retriever-chesapeake.jpeg', 'availability': 'Available', 'description': 'An American breed known for its love of water and retrieving.', 'date_created': dog_shared_date3},
            {'type_name': 'Dog', 'breed_name': 'Rhodesian Ridgeback', 'dispositions': ['Good with other animals', 'Animal must be leashed at all times', 'Good with children'], 'pic': 'app/images/dogs/ridgeback-rhodesian.jpeg', 'availability': 'Available', 'description': 'Originally bred to hunt lions, this dog is both strong-willed and affectionate.', 'date_created': dog_shared_date5},
            {'type_name': 'Dog', 'breed_name': 'Old English Sheepdog', 'dispositions': ['Animal must be leashed at all times'], 'pic': 'app/images/dogs/sheepdog-english.jpeg', 'availability': 'Available', 'description': 'A large breed with a shaggy coat, known for its gentle nature.', 'date_created': dog_shared_date5},
            {'type_name': 'Dog', 'breed_name': 'Jack Russell Terrier', 'dispositions': ['Animal must be leashed at all times', 'Good with children'], 'pic': 'app/images/dogs/terrier-russell.jpeg', 'availability': 'Available', 'description': 'A small terrier that is known for its athleticism and fearlessness.', 'date_created': dog_shared_date1},
            {'type_name': 'Dog', 'breed_name': 'Tibetan Terrier', 'dispositions': ['Good with other animals', 'Good with children', 'Animal must be leashed at all times'], 'pic': 'app/images/dogs/terrier-tibetan.jpeg', 'availability': 'Available', 'description': 'Often mistaken for a sheepdog, this terrier is affectionate and sensitive.', 'date_created': dog_shared_date4},
            {'type_name': 'Dog', 'breed_name': 'Welsh Terrier', 'dispositions': ['Good with other animals', 'Animal must be leashed at all times'], 'pic': 'app/images/dogs/terrier-welsh.jpeg', 'availability': 'Available', 'description': 'This breed is known for its friendly nature and intelligent spirit.', 'date_created': dog_shared_date2},
        ]

        # Iterate over the animals_data list and create AnimalProfile objects
        for animal_data in animals_data:
            with open(animal_data['pic'], 'rb') as image_file:
                # Read the image file and encode it to binary
                pic_binary = binary.Binary(image_file.read())

            animal = AnimalProfile(
                profile_id=None,
                type_name=animal_data['type_name'],
                breed_name=animal_data['breed_name'],
                dispositions=animal_data['dispositions'],
                pic=pic_binary,  # Store the binary data of the picture
                availability=animal_data['availability'],
                description=animal_data['description'],
                date_created = animal_data['date_created'],
                adoption_hooman=None,
            )

            # Insert the animal profile into the database
            insert_animal_profile(animal.to_document())
        
    with app.app_context():
        if not get_db_flag('animals_loaded'):
            create_animal_profiles()  # Load animals
            set_db_flag('animals_loaded', True)  # Set the flag to True       

    # Run the create_admin_user function before the first request
    with app.app_context():
        create_admin_user()

    return app
