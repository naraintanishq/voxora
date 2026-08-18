from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config import supabase_client

# This tells FastAPI where the client will send the token.
# The `tokenUrl` points to our own login endpoint.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency to get the current user from a JWT token.
    This will be used to protect our endpoints.
    """
    try:
        # Supabase's `get_user` method validates the token and returns the user
        user = supabase_client.auth.get_user(token).user
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )