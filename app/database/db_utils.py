from .db import mongo
from bson.objectid import ObjectId


def find_user_by_username(username):
    return mongo.db.hoomans.find_one({"username": username})

def insert_animal_profile(animal_profile):
    return mongo.db.animal_profiles.insert_one(animal_profile.to_document())

def insert_hooman(hooman_data):
    return mongo.db.hoomans.insert_one(hooman_data)

def find_animal_profile(profile_id):
    return mongo.db.animal_profiles.find_one({"_id": profile_id})

def update_animal_profile(profile_id, update_data):
    return mongo.db.animal_profiles.update_one({"_id": profile_id}, {"$set": update_data})

def delete_animal_profile(profile_id):
    return mongo.db.animal_profiles.delete_one({"_id": profile_id})

def find_hooman(hooman_id):
    # Convert string to ObjectId, assuming hooman_id is passed as a string
    if isinstance(hooman_id, str):
        try:
            hooman_id = ObjectId(hooman_id)
        except:
            return None  # Handle invalid ObjectId string

    hooman = mongo.db.hoomans.find_one({"_id": hooman_id})
    if hooman:
        # Convert ObjectId fields (_id and adoption_history) to strings for serialization
        hooman['_id'] = str(hooman['_id'])
        if 'adoption_history' in hooman:
            hooman['adoption_history'] = [str(animal_id) for animal_id in hooman['adoption_history']]
        return hooman
    else:
        return None

def update_hooman(hooman_id, update_data):
    return mongo.db.hoomans.update_one({"_id": hooman_id}, {"$set": update_data})

def delete_hooman(hooman_id):
    return mongo.db.hoomans.delete_one({"_id": hooman_id})

def find_hooman_by_id(hooman_id):
    try:
        # Ensure hooman_id is an ObjectId
        obj_id = ObjectId(hooman_id)
    except:
        return None  # Handle invalid ObjectId string

    hooman = mongo.db.hoomans.find_one({"_id": obj_id})
    if hooman:
        # Convert ObjectId back to string for _id
        hooman['_id'] = str(hooman['_id'])
        if 'adoption_history' in hooman:
            # Convert ObjectId's to strings for adoption_history, if it's present
            hooman['adoption_history'] = [str(animal_id) for animal_id in hooman['adoption_history']]
        return hooman
    else:
        return None
    
def find_user_by_email(email):
    return mongo.db.hoomans.find_one({"email": email})

def get_all_users():
    users_cursor = mongo.db.hoomans.find()
    users = list(users_cursor)
    # Convert ObjectId fields (_id and potentially others) to strings for serialization
    for user in users:
        user['_id'] = str(user['_id'])
        if 'adoption_history' in user:
            user['adoption_history'] = [str(animal_id) for animal_id in user['adoption_history']]
    return users
