from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List, Dict, Any
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


class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float
    name: str


class OrderBase(BaseModel):
    items: List[OrderItem]
    total: float
    shipping_address: str
    phone_number: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [
                    {
                        "product_id": "60d5ec9af3857d1b4bfe0b6c",
                        "quantity": 2,
                        "price": 5000000,
                        "name": "Điện thoại XYZ"
                    }
                ],
                "total": 10000000,
                "shipping_address": "123 Đường ABC, Quận XYZ, Hà Nội",
                "phone_number": "0123456789"
            }
        }
    }


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: str


class OrderInDB(OrderBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    status: str = "pending"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "_id": "60d5ec9af3857d1b4bfe0b6c",
                "items": [
                    {
                        "product_id": "60d5ec9af3857d1b4bfe0b6c",
                        "quantity": 2,
                        "price": 5000000,
                        "name": "Điện thoại XYZ"
                    }
                ],
                "total": 10000000,
                "shipping_address": "123 Đường ABC, Quận XYZ, Hà Nội",
                "phone_number": "0123456789",
                "user_id": "60d5ec9af3857d1b4bfe0b6d",
                "status": "pending",
                "created_at": "2023-10-30T12:00:00",
                "updated_at": "2023-10-30T12:00:00"
            }
        }
    }

    @field_serializer('id')
    def serialize_id(self, value):
        return str(value)

    @field_serializer('user_id')
    def serialize_user_id(self, value):
        return str(value)


class OrderResponse(OrderBase):
    id: str = Field(..., alias="_id")
    user_id: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "_id": "60d5ec9af3857d1b4bfe0b6c",
                "items": [
                    {
                        "product_id": "60d5ec9af3857d1b4bfe0b6c",
                        "quantity": 2,
                        "price": 5000000,
                        "name": "Điện thoại XYZ"
                    }
                ],
                "total": 10000000,
                "shipping_address": "123 Đường ABC, Quận XYZ, Hà Nội",
                "phone_number": "0123456789",
                "user_id": "60d5ec9af3857d1b4bfe0b6d",
                "status": "pending",
                "created_at": "2023-10-30T12:00:00",
                "updated_at": "2023-10-30T12:00:00"
            }
        }
    }