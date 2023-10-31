from datetime import datetime

class PetProfile:
    def __init__(self, type, breed, disposition, picture, availability, news_item, description):
        self.type = type
        self.breed = breed
        self.disposition = disposition
        self.picture = picture
        self.availability = availability
        self.news_item = news_item
        self.description = description
        self.date_created = datetime.utcnow()
