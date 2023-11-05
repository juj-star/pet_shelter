from datetime import datetime
from bson import ObjectId

class AnimalProfile:
    def __init__(self, profile_id, type_name, breed_name, dispositions, pic, availability, description, date_created=None):
        self._id = ObjectId(profile_id) if profile_id else ObjectId()
        self.type_name = type_name  # e.g., "Dog", "Cat", "Other"
        self.breed_name = breed_name  # e.g., "Golden Retriever", "Other"
        self.dispositions = dispositions  # List of dispositions, e.g., ["Good with children", "Needs leash"]
        self.pic = pic  # URL or path to the picture
        self.availability = availability  # e.g., "Available"
        self.description = description
        self.date_created = date_created or datetime.utcnow()  # Set current time if not provided

    def to_document(self):
        # Convert instance variables to a dictionary for MongoDB insertion
        # Convert ObjectId to string and datetime to a string if required
        document = {
            '_id': str(self._id),
            'type_name': self.type_name,
            'breed_name': self.breed_name,
            'dispositions': self.dispositions,
            'pic': self.pic,
            'availability': self.availability,
            'description': self.description,
            'date_created': self.date_created.isoformat() if isinstance(self.date_created, datetime) else self.date_created
        }
        return document

    def display_info(self):
        # Print out the animal profile information
        print(f"Animal Profile ID: {str(self._id)}")
        print(f"Type: {self.type_name}")
        print(f"Breed: {self.breed_name}")
        print(f"Dispositions: {', '.join(self.dispositions)}")
        print(f"Picture URL: {self.pic}")
        print(f"Availability: {self.availability}")
        print(f"Description: {self.description}")
        print(f"Date Created: {self.date_created}")
