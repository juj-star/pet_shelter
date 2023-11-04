from bson import ObjectId

class Hooman:
    def __init__(self, hooman_id, name, email, phone, address, is_admin=False, adoption_history=[]):
        self._id = ObjectId(hooman_id) if hooman_id else ObjectId()
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.is_admin = is_admin  # Indicates whether the hooman is an admin
        self.adoption_history = adoption_history  # List of animal profile IDs adopted previously

    def to_document(self):
        # When converting to a document, ensure to convert _id to string if it's meant to be JSON serializable
        document = self.__dict__.copy()
        document['_id'] = str(self._id)  # Convert ObjectId to string for JSON serialization
        return document

    def display_info(self):
        print(f"Hooman ID: {str(self._id)}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Phone: {self.phone}")
        print(f"Address: {self.address}")
        print(f"Admin: {'Yes' if self.is_admin else 'No'}")  # Display if the hooman is an admin
        print(f"Adoption History: {self.adoption_history}")
