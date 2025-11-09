from app.models.Base_model import BaseModel

class Amenity(BaseModel):
    
    def __init__(self, name):
        super().__init__()
        self.set_name(name)


    def set_name(self, value):
        if not isinstance(value, str) or len(value) > 50 or not value:
            raise ValueError("Name must be a non-empty string <= 50 characters.")
        self.name = value
        self.save()