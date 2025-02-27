from fastapi import APIRouter,Depends
from .token_release import check_token


router = APIRouter()


@router.get("/test_token")
def test(stored_user = Depends(check_token)):
    return "Hello,token is work"