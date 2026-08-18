from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """Data model for creating a new user."""
    email: EmailStr  # EmailStr is a special Pydantic type that validates the email format.
    password: str

class UserResponse(BaseModel):
    """Data model for the response after a user is created."""
    id: str
    email: EmailStr

    class Config:
        from_attributes = True # Formerly orm_mode = True


# (Keep the UserCreate and UserResponse classes at the top)

class UserLogin(BaseModel):
    """Data model for a user logging in."""
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """Data model for the response containing the access token."""
    access_token: str
    token_type: str = "bearer"