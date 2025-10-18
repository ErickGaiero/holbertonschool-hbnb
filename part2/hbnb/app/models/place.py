from models.Base_model import BaseModel
from models.user import User
from models.review import Review
from models.amenity import Amenity

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.set_title = title
        self.set_description = description
        self.set_price = price
        self.set_latitude = latitude
        self.set_longitude = longitude
        self.set_owner = owner
        self.reviews = []
        self.amenities = []

    def set_title(self, value):
        if not isinstance(value, str) or len(value) > 100 or not value:
            raise ValueError("Title must be a non-empty string <= 100 characters.")
        self.title = value
        self.save()

    def set_description(self, value):
        if not isinstance(value, str):
            raise ValueError("Description must be a string.")
        self.description = value
        self.save()

    def set_price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a positive number.")
        self.price = value
        self.save()

    def set_latitude(self, value):
        if not isinstance(value, (int, float)) or not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        self.latitude = value
        self.save()

    def set_longitude(self, value):
        if not isinstance(value, (int, float)) or not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        self.longitude = value
        self.save()

    def set_owner(self, value):
        if not isinstance(value, User):
            raise ValueError("Owner must be a User instance.")
        self.owner = value
        self.save()

    def add_review(self, review):
        if not isinstance(review, Review):
            raise ValueError("Review must be a Review instance.")
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise ValueError("Amenity must be an Amenity instance.")
        self.amenities.append(amenity)
        self.save()
