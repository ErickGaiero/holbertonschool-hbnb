from email_validator import validate_email, EmailNotValidError
from app.models.Base_model import BaseModel


unique_emails = set()

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.set_first_name = first_name
        self.set_last_name = last_name
        self.set_email = email
        self.set_is_admin = is_admin

    def set_first_name(self, value):
        if not isinstance(value, str) or len(value) > 50 or not value:
            raise ValueError("First name must be a non-empty string <= 50 characters.")
        self.first_name = value
        self.save()

    def set_last_name(self, value):
        if not isinstance(value, str) or len(value) > 50 or not value:
            raise ValueError("Last name must be a non-empty string <= 50 characters.")
        self.last_name = value
        self.save()

    def set_email(self, value):
        try:
            validate_email(value, check_deliverability=False)
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email format: {str(e)}")

        if value in unique_emails:
            raise ValueError("Email must be unique.")
        unique_emails.add(value)
        self.email = value
        self.save()

    def set_is_admin(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean.")
        self.is_admin = value
        self.save()
