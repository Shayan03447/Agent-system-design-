"""User HTTP API."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from apps.api.db import models
from apps.api.db.session import get_db
from apps.api.schemas.user import UserCreate, UserRead

router = APIRouter()


class ErrorResponse(BaseModel):
    detail: str


@router.post(
    "",
    response_model=UserRead,
    responses={409: {"model": ErrorResponse}},
    summary="Register a user by email",
)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> models.User:
    normalized = payload.email.strip().lower()
    user = models.User(email=normalized)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        ) from None
    db.refresh(user)
    return user


@router.get("", response_model=list[UserRead], summary="List users (newest first by id)")
def list_users(db: Session = Depends(get_db)) -> list[models.User]:
    stmt = select(models.User).order_by(models.User.id.desc())
    return list(db.scalars(stmt).all())
