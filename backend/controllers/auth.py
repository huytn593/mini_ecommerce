from fastapi import HTTPException, status
from bson.objectid import ObjectId
from datetime import datetime, UTC

from ..models.user import UserCreate, UserLogin, UserInDB, TokenResponse
from ..utils.auth import hash_password, verify_password, create_token
from ..utils.database import Database
from ..utils.logger import logger


async def register_user(user: UserCreate):
    # Check if email already exists
    if await Database.db.users.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã tồn tại trong hệ thống",
        )

    # Check if username already exists
    if await Database.db.users.find_one({"username": user.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên đăng nhập đã tồn tại trong hệ thống",
        )

    # Hash password
    hashed_password = hash_password(user.password)

    # Create a dictionary with user data excluding password
    user_dict = user.model_dump(exclude={"password"})

    user_dict.update({
        "password": hashed_password,
        "created_at": datetime.now(UTC)
    })

    # Create user document
    user_data = UserInDB(**user_dict)

    # Insert user into database
    result = await Database.db.users.insert_one(user_data.model_dump(by_alias=True))

    # Get created user
    created_user = await Database.db.users.find_one({"_id": result.inserted_id})

    logger.info(f"User registered: {user.username} with role {user.role}")

    # Return token
    return TokenResponse(
        access_token=create_token({
            "sub": str(created_user["_id"]),
            "username": created_user["username"],
            "role": created_user["role"]
        }),
        user_id=str(created_user["_id"]),
        username=created_user["username"],
        role=created_user["role"]
    )


async def login_user(user: UserLogin):
    # Find user by email
    db_user = await Database.db.users.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không đúng",
        )

    # Verify password
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không đúng",
        )

    logger.info(f"User logged in: {db_user['username']}")

    # Return token
    return TokenResponse(
        access_token=create_token({
            "sub": str(db_user["_id"]),
            "username": db_user["username"],
            "role": db_user["role"]
        }),
        user_id=str(db_user["_id"]),
        username=db_user["username"],
        role=db_user["role"]
    )


async def get_current_user(user_id: str):
    # Find user by id
    db_user = await Database.db.users.find_one({"_id": ObjectId(user_id)})

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại",
        )

    # Remove password from response
    db_user.pop("password", None)

    # Convert ObjectId to string
    db_user["_id"] = str(db_user["_id"])

    return db_user