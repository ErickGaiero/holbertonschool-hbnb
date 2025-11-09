from email_validator import validate_email, EmailNotValidError
from app.models.Base_model import BaseModel
from app.extenciones import bcrypt

unique_emails = set()

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.set_first_name(first_name)
        self.set_last_name(last_name)
        self.set_email(email)
        self.hash_password(password)
        self.is_admin = is_admin

    def set_first_name(self, value):
        if not isinstance(value, str) or not value or len(value) > 50:
            raise ValueError("First name must be a non-empty string <= 50 characters.")
        self.first_name = value
        self.save()

    def set_last_name(self, value):
        if not isinstance(value, str) or not value or len(value) > 50:
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

    def hash_password(self, password):
        """Hashes the password before storing it."""
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
