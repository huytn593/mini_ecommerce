from fastapi import HTTPException, status
from bson.objectid import ObjectId
from datetime import datetime
from typing import List, Optional

from ..utils.database import Database
from ..utils.logger import logger

async def get_seller_dashboard_stats(seller_id: str):
    # Get seller products
    cursor = Database.db.products.find({"seller_id": ObjectId(seller_id)})
    products = await cursor.to_list(length=None)
    product_ids = [str(product["_id"]) for product in products]
    
    # Get product count
    total_products = len(products)
    
    # Find orders containing seller products
    orders = []
    cursor = Database.db.orders.find({}).sort("created_at", -1)
    all_orders = await cursor.to_list(length=None)
    
    for order in all_orders:
        for item in order["items"]:
            if item["product_id"] in product_ids:
                orders.append(order)
                break
    
    # Get order count
    total_orders = len(orders)
    
    # Get total revenue
    total_revenue = 0
    for order in orders:
        if order["status"] != "cancelled":
            for item in order["items"]:
                if item["product_id"] in product_ids:
                    total_revenue += item["price"] * item["quantity"]
    
    # Get recent orders
    recent_orders = orders[:5]
    for order in recent_orders:
        order["_id"] = str(order["_id"])
        order["user_id"] = str(order["user_id"])
    
    # Get stock alerts (products with stock < 5)
    stock_alerts = []
    for product in products:
        if product["stock"] < 5:
            product["_id"] = str(product["_id"])
            product["seller_id"] = str(product["seller_id"])
            stock_alerts.append(product)
    
    return {
        "counts": {
            "total_products": total_products,
            "total_orders": total_orders,
            "total_revenue": total_revenue
        },
        "recent_orders": recent_orders,
        "stock_alerts": stock_alerts
    }
