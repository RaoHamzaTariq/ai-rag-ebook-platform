from fastapi import APIRouter, Depends, HTTPException
from ..dependencies.auth import get_current_user_id

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=dict)
async def get_current_user(user_id: str = Depends(get_current_user_id)):
    """
    Get the current authenticated user's information.
    """
    try:
        # Return the user ID as per the authentication system
        return {
            "user_id": user_id,
            "message": "User authenticated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user info: {str(e)}")