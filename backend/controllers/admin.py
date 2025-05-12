from fastapi import HTTPException, status as http_status
from bson.objectid import ObjectId
from datetime import datetime, UTC
from typing import List, Optional

from ..utils.database import Database
from ..utils.logger import logger


async def get_all_users(limit: int = 10, skip: int = 0, role: Optional[str] = None):
    # Build query
    query = {}
    if role:
        query["role"] = role

    # Query database
    cursor = Database.db.users.find(query).sort("created_at", -1).skip(skip).limit(limit)
    users = await cursor.to_list(length=limit)

    # Convert ObjectId to string and remove password
    for user in users:
        user["_id"] = str(user["_id"])
        user.pop("password", None)

    return users


async def delete_user(user_id: str):
    try:
        # Find user by id
        user = await Database.db.users.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Người dùng không tồn tại",
            )

        # Delete user
        await Database.db.users.delete_one({"_id": ObjectId(user_id)})

        logger.info(f"User deleted: {user_id}")

        return {"message": "Người dùng đã được xóa thành công"}
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"ID người dùng không hợp lệ: {str(e)}",
        )


async def update_user_role(user_id: str, role: str):
    try:
        # Find user by id
        user = await Database.db.users.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Người dùng không tồn tại",
            )

        # Update user role
        await Database.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"role": role}}
        )

        # Get updated user
        updated_user = await Database.db.users.find_one({"_id": ObjectId(user_id)})

        logger.info(f"User {user_id} role updated to {role}")

        # Convert ObjectId to string and remove password
        updated_user["_id"] = str(updated_user["_id"])
        updated_user.pop("password", None)

        return updated_user
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"ID người dùng không hợp lệ: {str(e)}",
        )


async def get_all_reports(limit: int = 10, skip: int = 0, report_status: Optional[str] = None):
    # Build query
    query = {}
    if report_status:
        query["status"] = report_status

    # Query database
    cursor = Database.db.reports.find(query).sort("created_at", -1).skip(skip).limit(limit)
    reports = await cursor.to_list(length=limit)

    # Convert ObjectId to string
    for report in reports:
        report["_id"] = str(report["_id"])
        report["user_id"] = str(report["user_id"])

    return reports


async def update_report_status(report_id: str, report_status: str):
    try:
        # Find report by id
        report = await Database.db.reports.find_one({"_id": ObjectId(report_id)})

        if not report:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Báo cáo không tồn tại",
            )

        # Update report status
        await Database.db.reports.update_one(
            {"_id": ObjectId(report_id)},
            {"$set": {"status": report_status}}
        )

        # Get updated report
        updated_report = await Database.db.reports.find_one({"_id": ObjectId(report_id)})

        logger.info(f"Report {report_id} status updated to {report_status}")

        # Convert ObjectId to string
        updated_report["_id"] = str(updated_report["_id"])
        updated_report["user_id"] = str(updated_report["user_id"])

        return updated_report
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"ID báo cáo không hợp lệ: {str(e)}",
        )


async def get_dashboard_stats():
    # Get counts
    total_users = await Database.db.users.count_documents({})
    total_products = await Database.db.products.count_documents({})
    total_orders = await Database.db.orders.count_documents({})
    total_reports = await Database.db.reports.count_documents({})

    # Get recent users
    cursor = Database.db.users.find({}).sort("created_at", -1).limit(5)
    recent_users = await cursor.to_list(length=5)
    for user in recent_users:
        user["_id"] = str(user["_id"])
        user.pop("password", None)

    # Get recent orders
    cursor = Database.db.orders.find({}).sort("created_at", -1).limit(5)
    recent_orders = await cursor.to_list(length=5)
    for order in recent_orders:
        order["_id"] = str(order["_id"])
        order["user_id"] = str(order["user_id"])

    # Get pending reports
    cursor = Database.db.reports.find({"status": "pending"}).sort("created_at", -1).limit(5)
    pending_reports = await cursor.to_list(length=5)
    for report in pending_reports:
        report["_id"] = str(report["_id"])
        report["user_id"] = str(report["user_id"])

    return {
        "counts": {
            "total_users": total_users,
            "total_products": total_products,
            "total_orders": total_orders,
            "total_reports": total_reports
        },
        "recent_users": recent_users,
        "recent_orders": recent_orders,
        "pending_reports": pending_reports
    }