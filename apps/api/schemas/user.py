from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)


class UserRead(BaseModel):
    id: int
    email: str

    model_config = {"from_attributes": True}
