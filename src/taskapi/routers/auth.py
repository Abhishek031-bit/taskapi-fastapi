from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from taskapi.core.deps import DbSession
from taskapi.schemas.user import Token, UserCreate, UserRead
from taskapi.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def signup(data: UserCreate, db: DbSession):
    return await auth_service.signup(db, data)


@router.post("/login", response_model=Token)
async def login(
    db: DbSession, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    token = await auth_service.login(db, form_data.username, form_data.password)
    return Token(access_token=token)
