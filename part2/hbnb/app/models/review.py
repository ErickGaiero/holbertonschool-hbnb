from models.Base_model import BaseModel
from models.place import Place
from models.user import User

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.set_text(text)
        self.set_rating(rating)
        self.set_place(place)
        self.set_user(user)

    def set_text(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("Text must be a non-empty string.")
        self.text = value
        self.save()

    def set_rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        self.rating = value
        self.save()

    def set_place(self, value):
        if not isinstance(value, Place):
            raise ValueError("Place must be a Place instance.")
        self.place = value
        self.save()

    def set_user(self, value):
        if not isinstance(value, User):
            raise ValueError("User must be a User instance.")
        self.user = value
        self.save()
