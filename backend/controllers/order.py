from fastapi import HTTPException, status as http_status
from bson.objectid import ObjectId
from datetime import datetime, UTC
from typing import List, Optional

from ..models.order import OrderCreate, OrderUpdate, OrderInDB, PyObjectId
from ..utils.database import Database
from ..utils.logger import logger


async def create_order(order: OrderCreate, user_id: str):
    # Check product availability and update stock
    for item in order.items:
        product = await Database.db.products.find_one({"_id": ObjectId(item.product_id)})

        if not product:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail=f"Sản phẩm với ID {item.product_id} không tồn tại",
            )

        if product["stock"] < item.quantity:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail=f"Sản phẩm {product['name']} chỉ còn {product['stock']} trong kho",
            )

        # Update product stock
        await Database.db.products.update_one(
            {"_id": ObjectId(item.product_id)},
            {"$inc": {"stock": -item.quantity}}
        )

    order_data = OrderInDB(
        **order.model_dump(),
        user_id=PyObjectId(user_id),
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )

    # Insert order into database
    result = await Database.db.orders.insert_one(order_data.model_dump(by_alias=True))

    # Get created order
    created_order = await Database.db.orders.find_one({"_id": result.inserted_id})

    logger.info(f"Order created by user {user_id}")

    # Convert ObjectId to string
    created_order["_id"] = str(created_order["_id"])
    created_order["user_id"] = str(created_order["user_id"])

    return created_order


async def get_all_orders(limit: int = 10, skip: int = 0, order_status: Optional[str] = None):
    # Build query
    query = {}
    if order_status:
        query["status"] = order_status

    # Query database
    cursor = Database.db.orders.find(query).sort("created_at", -1).skip(skip).limit(limit)
    orders = await cursor.to_list(length=limit)

    # Convert ObjectId to string
    for order in orders:
        order["_id"] = str(order["_id"])
        order["user_id"] = str(order["user_id"])

    return orders


async def get_order_by_id(order_id: str):
    try:
        # Find order by id
        order = await Database.db.orders.find_one({"_id": ObjectId(order_id)})

        if not order:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Đơn hàng không tồn tại",
            )

        # Convert ObjectId to string
        order["_id"] = str(order["_id"])
        order["user_id"] = str(order["user_id"])

        return order
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"ID đơn hàng không hợp lệ: {str(e)}",
        )


async def update_order_status(order_id: str, order_update: OrderUpdate):
    try:
        # Find order by id
        order = await Database.db.orders.find_one({"_id": ObjectId(order_id)})

        if not order:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Đơn hàng không tồn tại",
            )

        # Update order status
        await Database.db.orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {
                "status": order_update.status,
                "updated_at": datetime.now(UTC)
            }}
        )

        # Get updated order
        updated_order = await Database.db.orders.find_one({"_id": ObjectId(order_id)})

        logger.info(f"Order {order_id} status updated to {order_update.status}")

        # Convert ObjectId to string
        updated_order["_id"] = str(updated_order["_id"])
        updated_order["user_id"] = str(updated_order["user_id"])

        return updated_order
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"ID đơn hàng không hợp lệ: {str(e)}",
        )


async def get_user_orders(user_id: str):
    # Find orders by user_id
    cursor = Database.db.orders.find({"user_id": ObjectId(user_id)}).sort("created_at", -1)
    orders = await cursor.to_list(length=100)

    # Convert ObjectId to string
    for order in orders:
        order["_id"] = str(order["_id"])
        order["user_id"] = str(order["user_id"])

    return orders


async def get_seller_orders(seller_id: str):
    # Get seller products
    cursor = Database.db.products.find({"seller_id": ObjectId(seller_id)})
    products = await cursor.to_list(length=None)
    product_ids = [str(product["_id"]) for product in products]

    # Find orders containing seller products
    orders = []
    cursor = Database.db.orders.find({}).sort("created_at", -1)
    all_orders = await cursor.to_list(length=None)

    for order in all_orders:
        for item in order["items"]:
            if item["product_id"] in product_ids:
                # Convert ObjectId to string
                order["_id"] = str(order["_id"])
                order["user_id"] = str(order["user_id"])
                orders.append(order)
                break

    return orders