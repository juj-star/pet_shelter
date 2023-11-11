from .db import mongo
from bson.objectid import ObjectId
from bson import Regex


def find_user_by_username(username):
    return mongo.db.hoomans.find_one({"username": username})

def insert_animal_profile(animal_profile):
    return mongo.db.animal_profiles.insert_one(animal_profile)

def insert_hooman(hooman_data):
    return mongo.db.hoomans.insert_one(hooman_data)

def find_animal_profile(profile_id):
    return mongo.db.animal_profiles.find_one({"_id": profile_id})

def update_animal_profile(profile_id, update_data):
    return mongo.db.animal_profiles.update_one({"_id": profile_id}, {"$set": update_data})

def delete_animal_profile(profile_id):
    return mongo.db.animal_profiles.delete_one({"_id": profile_id})

def find_hooman(hooman_id):
    hooman = mongo.db.hoomans.find_one({"_id": hooman_id})
    return hooman

def update_hooman(hooman_id, update_data):
    return mongo.db.hoomans.update_one({"_id": hooman_id}, {"$set": update_data})

def delete_hooman(hooman_id):
    return mongo.db.hoomans.delete_one({"_id": hooman_id})

def find_hooman_by_id(hooman_id):
    # No need to convert to ObjectId if the _id in the database is a string
    print(f"Looking for hooman with ID: {hooman_id}")  # Debugging print

    hooman = mongo.db.hoomans.find_one({"_id": hooman_id})
    if hooman:
        # Assuming _id is already a string, no conversion needed
        if 'adoption_history' in hooman:
            # Ensure adoption_history contains string IDs
            hooman['adoption_history'] = [str(animal_id) for animal_id in hooman['adoption_history']]
        return hooman
    else:
        print(f"Hooman not found in the database with ID: {hooman_id}")  # Debugging print
        return None
    
def find_user_by_email(email):
    return mongo.db.hoomans.find_one({"email": email})

def get_all_users():
    users = mongo.db.hoomans.find()
    users_list = []
    for user in users:
        #user['_id'] = str(user['_id'])  # Convert ObjectId to string
        users_list.append(user)
    return users_list

def get_available_animals():
    """
    Retrieves animal profiles from MongoDB where the 'availability' field is 'Available'.

    Returns:
        A list of dictionaries, where each dictionary represents an available animal profile.
    """
    available_animals_cursor = mongo.db.animal_profiles.find({'availability': 'Available'})
    # Convert the cursor to a list and return
    return list(available_animals_cursor)

def get_pending_animals():
    """
    Retrieves animal profiles from MongoDB where the 'availability' field is 'Pending'.

    Returns:
        A list of dictionaries, where each dictionary represents a pending animal profile.
    """
    pending_animals_cursor = mongo.db.animal_profiles.find({'availability': 'Pending'})
    return list(pending_animals_cursor)

def get_unavailable_animals():
    """
    Retrieves animal profiles from MongoDB where the 'availability' field is 'Unavailable'.

    Returns:
        A list of dictionaries, where each dictionary represents an unavailable animal profile.
    """
    unavailable_animals_cursor = mongo.db.animal_profiles.find({'availability': 'Unavailable'})
    return list(unavailable_animals_cursor)

def get_animals_by_type(type_name):
    """
    Retrieves animal profiles from MongoDB where the 'type_name' field matches the search term.

    Args:
        type_name (str): The type name to search for.

    Returns:
        list: A list of dictionaries, where each dictionary represents an animal profile.
    """
    # Use a case-insensitive regex search for flexibility
    regex = Regex(f"^{type_name}$", "i")
    animals_cursor = mongo.db.animal_profiles.find({'type_name': regex})
    return list(animals_cursor)

def get_animals_by_breed(breed_name):
    """
    Retrieves animal profiles from MongoDB where the 'breed_name' field matches the search term.

    Args:
        breed_name (str): The breed name to search for.

    Returns:
        list: A list of dictionaries, where each dictionary represents an animal profile.
    """
    # Use a case-insensitive regex search for flexibility
    regex = Regex(f"^{breed_name}$", "i")
    animals_cursor = mongo.db.animal_profiles.find({'breed_name': regex})
    return list(animals_cursor)
