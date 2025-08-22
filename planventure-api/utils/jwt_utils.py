from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
import jwt
from flask import current_app

class JWTManager:
    """JWT token generation and validation utility class"""
    
    ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # 1 hour
    REFRESH_TOKEN_EXPIRES = timedelta(days=7)  # 7 days
    
    @staticmethod
    def generate_tokens(user_id: int) -> Dict[str, str]:
        """
        Generates access and refresh tokens for a user
        """
        access_token = JWTManager._generate_token(
            user_id, 
            JWTManager.ACCESS_TOKEN_EXPIRES,
            token_type="access"
        )
        
        refresh_token = JWTManager._generate_token(
            user_id, 
            JWTManager.REFRESH_TOKEN_EXPIRES,
            token_type="refresh"
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    @staticmethod
    def _generate_token(user_id: int, expires_delta: timedelta, token_type: str) -> str:
        """
        Creates a JWT token with claims
        """
        now = datetime.now(timezone.utc)
        claims = {
            "sub": user_id,  # subject (user id)
            "type": token_type,
            "iat": now,  # issued at
            "exp": now + expires_delta,  # expiration
        }
        
        return jwt.encode(
            claims,
            current_app.config["JWT_SECRET_KEY"],
            algorithm="HS256"
        )
    
    @staticmethod
    def decode_token(token: str) -> Optional[Dict]:
        """
        Decodes and validates a JWT token
        Returns None if token is invalid
        """
        try:
            return jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"]
            )
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def verify_access_token(token: str) -> Optional[int]:
        """
        Verifies an access token and returns the user ID if valid
        """
        claims = JWTManager.decode_token(token)
        if (claims and 
            claims.get("type") == "access" and
            datetime.fromtimestamp(claims["exp"], tz=timezone.utc) > datetime.now(timezone.utc)):
            return claims["sub"]
        return None