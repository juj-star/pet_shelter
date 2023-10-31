from bson import ObjectId

class AnimalType:
    def __init__(self, type_id, type_name):
        self.type_id = type_id
        self.type_name = type_name

class Breed:
    def __init__(self, breed_id, breed_name):
        self.breed_id = breed_id
        self.breed_name = breed_name

class Disposition:
    def __init__(self, disposition_id, disposition_name):
        self.disposition_id = disposition_id
        self.disposition_name = disposition_name

class Availability:
    def __init__(self, availability_id, availability_name):
        self.availability_id = availability_id
        self.availability_name = availability_name

class AnimalProfile:
    def __init__(self, profile_id, type_obj, breed_obj, disposition_obj, pic, availability_obj, description):
        self._id = ObjectId(profile_id) if profile_id else ObjectId()
        self.type = {
            "type_id": type_obj.type_id,
            "type_name": type_obj.type_name
        }
        self.breed = {
            "breed_id": breed_obj.breed_id,
            "breed_name": breed_obj.breed_name
        }
        self.disposition = {
            "disposition_id": disposition_obj.disposition_id,
            "disposition_name": disposition_obj.disposition_name
        }
        self.pic = pic
        self.availability = {
            "availability_id": availability_obj.availability_id,
            "availability_name": availability_obj.availability_name
        }
        self.description = description

    def display_info(self):
        print(f"Profile ID: {str(self._id)}")
        print(f"Type: {self.type['type_name']}")
        print(f"Breed: {self.breed['breed_name']}")
        print(f"Disposition: {self.disposition['disposition_name']}")
        print(f"Picture: {self.pic}")
        print(f"Availability: {self.availability['availability_name']}")
        print(f"Description: {self.description}")

    def to_document(self):
        return self.__dict__
