from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List, Any
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


class ProductBase(BaseModel):
    name: str
    price: float
    description: str
    category: str
    stock: int
    location: str
    images: List[str] = []

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Điện thoại XYZ",
                "price": 5000000,
                "description": "Điện thoại XYZ đời mới nhất",
                "category": "Điện thoại",
                "stock": 10,
                "location": "Hà Nội",
                "images": ["image1.jpg", "image2.jpg"]
            }
        }
    }


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    stock: Optional[int] = None
    location: Optional[str] = None
    images: Optional[List[str]] = None


class ProductInDB(ProductBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    seller_id: PyObjectId
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "_id": "60d5ec9af3857d1b4bfe0b6c",
                "name": "Điện thoại XYZ",
                "price": 5000000,
                "description": "Điện thoại XYZ đời mới nhất",
                "category": "Điện thoại",
                "stock": 10,
                "location": "Hà Nội",
                "images": ["image1.jpg", "image2.jpg"],
                "seller_id": "60d5ec9af3857d1b4bfe0b6d",
                "created_at": "2023-10-30T12:00:00",
                "updated_at": "2023-10-30T12:00:00"
            }
        }
    }

    @field_serializer('id')
    def serialize_id(self, value):
        return str(value)

    @field_serializer('seller_id')
    def serialize_seller_id(self, value):
        return str(value)


class ProductResponse(ProductBase):
    id: str = Field(..., alias="_id")
    seller_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "_id": "60d5ec9af3857d1b4bfe0b6c",
                "name": "Điện thoại XYZ",
                "price": 5000000,
                "description": "Điện thoại XYZ đời mới nhất",
                "category": "Điện thoại",
                "stock": 10,
                "location": "Hà Nội",
                "images": ["image1.jpg", "image2.jpg"],
                "seller_id": "60d5ec9af3857d1b4bfe0b6d",
                "created_at": "2023-10-30T12:00:00",
                "updated_at": "2023-10-30T12:00:00"
            }
        }
    }


class ReviewBase(BaseModel):
    product_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "product_id": "60d5ec9af3857d1b4bfe0b6c",
                "rating": 5,
                "comment": "Sản phẩm rất tốt"
            }
        }
    }


class ReviewCreate(ReviewBase):
    pass


class ReviewInDB(ReviewBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "_id": "60d5ec9af3857d1b4bfe0b6c",
                "product_id": "60d5ec9af3857d1b4bfe0b6c",
                "user_id": "60d5ec9af3857d1b4bfe0b6d",
                "rating": 5,
                "comment": "Sản phẩm rất tốt",
                "created_at": "2023-10-30T12:00:00"
            }
        }
    }

    @field_serializer('id')
    def serialize_id(self, value):
        return str(value)

    @field_serializer('user_id')
    def serialize_user_id(self, value):
        return str(value)


class ReviewResponse(ReviewBase):
    id: str = Field(..., alias="_id")
    user_id: str
    created_at: datetime

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "_id": "60d5ec9af3857d1b4bfe0b6c",
                "product_id": "60d5ec9af3857d1b4bfe0b6c",
                "user_id": "60d5ec9af3857d1b4bfe0b6d",
                "rating": 5,
                "comment": "Sản phẩm rất tốt",
                "created_at": "2023-10-30T12:00:00"
            }
        }
    }


class ReportBase(BaseModel):
    product_id: str
    reason: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "product_id": "60d5ec9af3857d1b4bfe0b6c",
                "reason": "Sản phẩm không đúng mô tả"
            }
        }
    }


class ReportCreate(ReportBase):
    pass


class ReportInDB(ReportBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    status: str = "pending"

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "_id": "60d5ec9af3857d1b4bfe0b6c",
                "product_id": "60d5ec9af3857d1b4bfe0b6c",
                "user_id": "60d5ec9af3857d1b4bfe0b6d",
                "reason": "Sản phẩm không đúng mô tả",
                "created_at": "2023-10-30T12:00:00",
                "status": "pending"
            }
        }
    }

    @field_serializer('id')
    def serialize_id(self, value):
        return str(value)

    @field_serializer('user_id')
    def serialize_user_id(self, value):
        return str(value)


class ReportResponse(ReportBase):
    id: str = Field(..., alias="_id")
    user_id: str
    created_at: datetime
    status: str

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "_id": "60d5ec9af3857d1b4bfe0b6c",
                "product_id": "60d5ec9af3857d1b4bfe0b6c",
                "user_id": "60d5ec9af3857d1b4bfe0b6d",
                "reason": "Sản phẩm không đúng mô tả",
                "created_at": "2023-10-30T12:00:00",
                "status": "pending"
            }
        }
    }