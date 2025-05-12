from pydantic import BaseModel, EmailStr, Field, field_serializer
from typing import Optional, List, Literal, Any
from datetime import datetime, UTC
from bson import ObjectId
from pydantic.json_schema import JsonSchemaValue


class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId")
            return ObjectId(v)
        return v

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema_generator, _field_schema) -> JsonSchemaValue:
        return {"type": "string"}


class UserBase(BaseModel):
    username: str
    email: EmailStr

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "user1",
                "email": "user@example.com"
            }
        }
    }


class UserCreate(UserBase):
    password: str
    role: Literal["user", "seller", "admin"] = "user"

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "user1",
                "email": "user@example.com",
                "password": "securepassword",
                "role": "user"
            }
        }
    }


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "securepassword"
            }
        }
    }


class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    role: str = "user"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "_id": "60d5ec9af3857d1b4bfe0b6c",
                "username": "user1",
                "email": "user@example.com",
                "role": "user",
                "created_at": "2023-10-30T12:00:00"
            }
        }
    }

    @field_serializer('id')
    def serialize_id(self, value):
        return str(value)


class UserResponse(UserBase):
    id: str = Field(..., alias="_id")
    role: str
    created_at: datetime

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "_id": "60d5ec9af3857d1b4bfe0b6c",
                "username": "user1",
                "email": "user@example.com",
                "role": "user",
                "created_at": "2023-10-30T12:00:00"
            }
        }
    }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str
    role: str