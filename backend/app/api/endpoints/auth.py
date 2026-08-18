from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ...config import supabase_client
from ...schemas import UserCreate, TokenResponse
# Create a new router for authentication endpoints
router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """
    Handles the creation of a new user in Supabase Auth and our public.users table.
    """
    try:
        # Step 1: Create the user in Supabase's built-in 'auth.users' table
        auth_response = supabase_client.auth.sign_up({
            "email": user.email,
            "password": user.password,
        })
        
        # Check if the user was created successfully in the auth schema
        if not auth_response.user:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create user in auth.")

        new_user = auth_response.user

        # Step 2: Create a corresponding entry in our public 'users' table
        # This is where we will store public profile info and the Stripe ID later
        user_profile_data = {
            "id": new_user.id,
            "email": new_user.email
            # We can add signup_ip_address here later
        }
        
        profile_response = supabase_client.table('users').insert(user_profile_data).execute()

        if profile_response.data is None:
            # This is a critical failure state - the auth user exists but our public profile doesn't.
            # In a real production app, you'd have a cleanup task or alert for this.
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create user profile.")

        # Step 3: Automatically create a personal team for the new user
        team_data = {
            "name": f"{new_user.email.split('@')[0]}'s Team" # e.g., "johnsdoe's Team"
        }
        team_response = supabase_client.table('teams').insert(team_data).execute()
        
        if not team_response.data:
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create personal team for user.")
             
        new_team = team_response.data[0]
        
        # Step 4: Link the user to their new team as the 'owner'
        team_member_data = {
            "user_id": new_user.id,
            "team_id": new_team['id'],
            "role": "owner"
        }
        member_response = supabase_client.table('team_members').insert(team_member_data).execute()
        
        if not member_response.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not link user to personal team.")


        return {"message": "User created successfully. Please check your email to verify your account."}

    except Exception as e:
        # Catch potential exceptions from Supabase, like if the user already exists
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    



@router.post("/login", response_model=TokenResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Handles user login using form data and returns a JWT access token.
    """
    try:
        # The form_data object has 'username' and 'password' attributes.
        # We use form_data.username because that's what OAuth2 specifies.
        auth_response = supabase_client.auth.sign_in_with_password({
            "email": form_data.username, # Use form_data.username as the email
            "password": form_data.password
        })

        session = auth_response.session
        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        return {
            "access_token": session.access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid credentials: {e}",
        )