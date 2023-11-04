from pymongo import MongoClient
from bson import ObjectId
from faker import Faker
import random

fake = Faker()

# Assuming the Hooman class is defined in a module named `hooman_module.py`
# from hooman_module import Hooman  # Uncomment and replace with your actual import

class Hooman:
    def __init__(self, name, email, phone, address, is_admin=False, adoption_history=[]):
        self._id = ObjectId()
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.is_admin = is_admin
        self.adoption_history = adoption_history

    def to_document(self):
        document = self.__dict__.copy()
        document['_id'] = str(self._id)  # Convert ObjectId to string for JSON serialization
        return document

# Function to insert a Hooman into MongoDB
def insert_hooman(hooman_doc):
    # Connect to the MongoDB database
    client = MongoClient('mongodb://localhost:27017/')
    db = client.pet_shelter
    hoomans = db.hoomans
    
    # Insert the document
    hoomans.insert_one(hooman_doc)

# Generate and insert 10 test users
for _ in range(10):
    name = fake.name()
    email = fake.email()
    phone = fake.phone_number()
    address = fake.address()
    hooman = Hooman(name, email, phone, address)
    hooman_doc = hooman.to_document()
    
    insert_hooman(hooman_doc)
    print(f"Inserted test hooman: {hooman_doc['name']} - ID: {hooman_doc['_id']}")
