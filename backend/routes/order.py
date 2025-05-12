from fastapi import APIRouter, Depends, Body, Query, Path
from typing import Optional, List
from ..models.order import OrderCreate, OrderUpdate
from ..controllers import order
from ..utils.auth import verify_token, seller_required, admin_required

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("")
async def create_order(
    order_data: OrderCreate = Body(...),
    payload: dict = Depends(verify_token)
):
    return await order.create_order(order_data, payload["sub"])

@router.get("/admin/all")
async def get_all_orders(
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    status: Optional[str] = Query(None),
    payload: dict = Depends(admin_required)
):
    return await order.get_all_orders(limit, skip, status)

@router.get("/{order_id}")
async def get_order_by_id(
    order_id: str = Path(...),
    payload: dict = Depends(verify_token)
):
    return await order.get_order_by_id(order_id)

@router.put("/{order_id}/status")
async def update_order_status(
    order_id: str = Path(...),
    order_update: OrderUpdate = Body(...),
    payload: dict = Depends(seller_required)
):
    return await order.update_order_status(order_id, order_update)

@router.get("/user/me")
async def get_user_orders(
    payload: dict = Depends(verify_token)
):
    return await order.get_user_orders(payload["sub"])

@router.get("/seller/me")
async def get_seller_orders(
    payload: dict = Depends(seller_required)
):
    return await order.get_seller_orders(payload["sub"])
