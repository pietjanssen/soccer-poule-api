from fastapi import APIRouter, Depends

from models.User import User
from tools.Firebase import get_current_user

router = APIRouter()


@router.get("/feyenoord")
def get_feyenoord_match_results(user: User = Depends(get_current_user)):
    """
    Get Feyenoord match results
    """

    return user