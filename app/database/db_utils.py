from .db import mongo
from bson.objectid import ObjectId
from bson import Regex
import base64


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

def get_all_animals():
    return mongo.db.animal_profiles.find()

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

def get_animals_by_search_term(search_term):
    """
    Searches for animal profiles in MongoDB where the search term matches
    the 'type_name', 'breed_name', 'dispositions', or 'date_created' fields.

    Args:
        search_term (str): The term to search for.

    Returns:
        list: A list of animal profiles that match the search term.
    """
    # Prepare a case-insensitive regex pattern
    regex_pattern = Regex(f".*{search_term}.*", "i")
    
    # Create a query that searches for the term in multiple fields
    query = {
        '$or': [
            {'type_name': regex_pattern},
            {'breed_name': regex_pattern},
            {'dispositions': regex_pattern},
            # For date_created, you might want to use a different approach
            # because it's likely stored in a date format. This is a simple
            # example that assumes date_created is a string that contains the year.
            {'date_created': regex_pattern}
        ]
    }
    
    # Execute the query to find matching animal profiles
    animals_cursor = mongo.db.animal_profiles.find(query)
    return list(animals_cursor)

def get_animals_by_query(query):
    """
    Retrieves animal profiles from MongoDB based on a query dictionary.
    Converts binary image data to base64 for HTML display.

    Args:
        query (dict): A dictionary containing query parameters for the search.

    Returns:
        list: A list of dictionaries, where each dictionary represents an animal profile.
    """
    animals_cursor = mongo.db.animal_profiles.find(query)
    animals = list(animals_cursor)

    # Convert binary image data to base64 string for each animal
    for animal in animals:
        if 'pic' in animal and animal['pic']:
            # Ensure the image data is in bytes and then convert to string
            if isinstance(animal['pic'], bytes):
                animal['pic'] = base64.b64encode(animal['pic']).decode('utf-8')
            else:
                # Handle cases where 'pic' might not be bytes (e.g., already a base64 string or None)
                pass

    return animals

def get_db_flag(flag_name):
    config_collection = mongo.db.get_collection('config')
    flag = config_collection.find_one({'flag_name': flag_name})
    return flag and flag.get('value', False)

def set_db_flag(flag_name, value):
    config_collection = mongo.db.get_collection('config')
    config_collection.update_one(
        {'flag_name': flag_name},
        {'$set': {'value': value}},
        upsert=True
    )

def get_adopted_animals():
    """
    Retrieves animal profiles from MongoDB where the 'availability' field is 'Adopted'.

    Returns:
        A list of dictionaries, where each dictionary represents an adopted animal profile.
    """
    adopted_animals_cursor = mongo.db.animal_profiles.find({'availability': 'Adopted'})
    # Convert the cursor to a list and return
    return list(adopted_animals_cursor)
