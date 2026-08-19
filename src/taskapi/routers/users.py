from fastapi import APIRouter

from taskapi.core.deps import CurrentUser
from taskapi.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: CurrentUser):
    return current_user
