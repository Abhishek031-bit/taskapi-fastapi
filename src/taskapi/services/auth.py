from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from taskapi.core.security import create_access_token, hash_password, verify_password
from taskapi.models import User
from taskapi.repositories import user as user_repo
from taskapi.schemas.user import UserCreate


async def signup(db: AsyncSession, data: UserCreate) -> User:
    existing = await user_repo.get_by_email(db, data.email)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )
    user = await user_repo.create_user(
        db,
        email=data.email,
        full_name=data.full_name,
        hashed_password=hash_password(data.password),
    )
    await db.commit()
    return user


async def login(db: AsyncSession, email: str, password: str) -> str:
    user = await user_repo.get_by_email(db, email)
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_access_token(subject=str(user.id))
