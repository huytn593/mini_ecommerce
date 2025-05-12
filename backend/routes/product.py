from fastapi import APIRouter, Depends, Body, Query, Path
from typing import Optional, List
from ..models.product import ProductCreate, ProductUpdate, ReviewCreate, ReportCreate
from ..controllers import product
from ..utils.auth import verify_token, seller_required, admin_required

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/search")
async def search_products(
    q: str = Query(..., description="Từ khóa tìm kiếm"),
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
):
    return await product.search_products(q, limit, skip, category, min_price, max_price, min_rating)

@router.post("")
async def create_product(
    product_data: ProductCreate = Body(...),
    payload: dict = Depends(seller_required)
):
    return await product.create_product(product_data, payload["sub"])

@router.get("")
async def get_all_products(
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None)
):
    return await product.get_all_products(limit, skip, category, search, sort_by)

@router.get("/{product_id}")
async def get_product_by_id(
    product_id: str = Path(...)
):
    return await product.get_product_by_id(product_id)

@router.put("/{product_id}")
async def update_product(
    product_id: str = Path(...),
    product_data: ProductUpdate = Body(...),
    payload: dict = Depends(seller_required)
):
    return await product.update_product(product_id, product_data, payload["sub"])

@router.delete("/{product_id}")
async def delete_product(
    product_id: str = Path(...),
    payload: dict = Depends(verify_token)
):
    is_admin = payload.get("role") == "admin"
    return await product.delete_product(product_id, payload["sub"], is_admin)

@router.get("/seller/me")
async def get_seller_products(
    payload: dict = Depends(seller_required)
):
    return await product.get_seller_products(payload["sub"])

@router.post("/reviews")
async def create_review(
    review: ReviewCreate = Body(...),
    payload: dict = Depends(verify_token)
):
    return await product.create_review(review, payload["sub"])

@router.get("/{product_id}/reviews")
async def get_product_reviews(
    product_id: str = Path(...)
):
    return await product.get_product_reviews(product_id)

@router.post("/reports")
async def create_report(
    report: ReportCreate = Body(...),
    payload: dict = Depends(verify_token)
):
    return await product.create_report(report, payload["sub"])
