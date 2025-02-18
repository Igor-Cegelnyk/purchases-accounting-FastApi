from fastapi import HTTPException
from pydantic import BaseModel, field_validator, root_validator
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from backend.config.exceptions.user import UsersException


class UserBase(BaseModel):
    first_name: str
    username: str

    @root_validator(pre=True)
    def validate_user(cls, values: dict) -> dict:
        first_name = values.get("first_name")
        username = values.get("username")
        if first_name and not (2 <= len(first_name) <= 25):
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail=UsersException.invalid_first_name,
            )
        if username and not (3 <= len(first_name) <= 50):
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail=UsersException.invalid_username,
            )
        return values


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not (8 <= len(value) <= 150):
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail=UsersException.invalid_password,
            )
        return value


class UserRead(UserBase):
    id: int

    model_config = {"from_attributes": True}
