from datetime import datetime, timezone
from flask import jsonify
from app import db
from utils.auth_utils import PasswordValidator
from typing import Optional, Tuple

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def set_password(self, password: str) -> Tuple[bool, Optional[str]]:
        """
        Sets user password with validation
        Returns: (success, error_message)
        """
        is_valid, error = PasswordValidator.validate_password(password)
        if not is_valid:
            return False, error
            
        self.password_hash = PasswordValidator.hash_password(password)
        return True, None

    def check_password(self, password: str) -> bool:
        """Verifies user password"""
        return PasswordValidator.verify_password(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<User {self.email}>'

# Example usage in registration route
def example_registration_route():
    user = User(email="example@example.com")  # Instantiate a User object with required fields
    password = "your_password_here"  # Define the password variable
    success, error = user.set_password(password)
    if not success:
        # from flask import jsonify  # Uncomment if jsonify is not already imported
        return jsonify({'error': error}), 400
    # Continue with registration logic...