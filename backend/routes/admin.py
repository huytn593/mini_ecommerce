from fastapi import APIRouter, Depends, Body, Query, Path
from typing import Optional, List
from ..controllers import admin
from ..utils.auth import admin_required

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users")
async def get_all_users(
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    role: Optional[str] = Query(None),
    payload: dict = Depends(admin_required)
):
    return await admin.get_all_users(limit, skip, role)

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str = Path(...),
    payload: dict = Depends(admin_required)
):
    return await admin.delete_user(user_id)

@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: str = Path(...),
    role_data: dict = Body(...),
    payload: dict = Depends(admin_required)
):
    return await admin.update_user_role(user_id, role_data["role"])

@router.get("/reports")
async def get_all_reports(
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    status: Optional[str] = Query(None),
    payload: dict = Depends(admin_required)
):
    return await admin.get_all_reports(limit, skip, status)

@router.put("/reports/{report_id}/status")
async def update_report_status(
    report_id: str = Path(...),
    status_data: dict = Body(...),
    payload: dict = Depends(admin_required)
):
    return await admin.update_report_status(report_id, status_data["status"])

@router.get("/dashboard")
async def get_dashboard_stats(
    payload: dict = Depends(admin_required)
):
    return await admin.get_dashboard_stats()
