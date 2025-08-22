import re
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Tuple, Optional

class PasswordValidator:
    """Password validation and hashing utility class"""
    
    MIN_LENGTH = 8
    HASH_METHOD = 'pbkdf2:sha256:260000'  # Using PBKDF2 with SHA256 and 260000 iterations
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, Optional[str]]:
        """
        Validates password strength
        Returns: (is_valid, error_message)
        """
        if len(password) < PasswordValidator.MIN_LENGTH:
            return False, f"Password must be at least {PasswordValidator.MIN_LENGTH} characters long"
        
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"
            
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"
            
        if not re.search(r"\d", password):
            return False, "Password must contain at least one number"
            
        if not re.search(r"[ !@#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password):
            return False, "Password must contain at least one special character"
            
        return True, None

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Creates a hashed password using PBKDF2 with SHA256
        """
        return generate_password_hash(password, method=PasswordValidator.HASH_METHOD)
    
    @staticmethod
    def verify_password(password_hash: str, password: str) -> bool:
        """
        Verifies if the password matches the hash
        """
        return check_password_hash(password_hash, password)