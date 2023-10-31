from bson import ObjectId

class Hooman:
    def __init__(self, hooman_id, name, email, phone, address, adoption_history=[]):
        self._id = ObjectId(hooman_id) if hooman_id else ObjectId()
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.adoption_history = adoption_history  # List of animal profile IDs adopted previously

    def to_document(self):
        return self.__dict__

    def display_info(self):
        print(f"Hooman ID: {str(self._id)}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Phone: {self.phone}")
        print(f"Address: {self.address}")
        print(f"Adoption History: {self.adoption_history}")
