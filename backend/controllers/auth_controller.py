from services.auth import authenticate_user as auth_service
from security.jwt_handler import create_access_token

def authenticate_user(username: str, password: str):
    """Authenticate user and return user data."""
    return auth_service(username, password)

def create_access_token(data: dict, expires_delta):
    """Generate JWT token."""
    return create_access_token(data, expires_delta)
