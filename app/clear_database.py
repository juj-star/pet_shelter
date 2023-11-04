from pymongo import MongoClient

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['pet_shelter']  # Use your actual database name

# Drop the collections
db['hoomans'].drop()  # Replace with your actual collection name
db['animals'].drop()  # Replace with your actual collection name for animals, etc.
