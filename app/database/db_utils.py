from .db import mongo

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
    return mongo.db.hoomans.find_one({"_id": hooman_id})

def update_hooman(hooman_id, update_data):
    return mongo.db.hoomans.update_one({"_id": hooman_id}, {"$set": update_data})

def delete_hooman(hooman_id):
    return mongo.db.hoomans.delete_one({"_id": hooman_id})
