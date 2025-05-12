from fastapi import APIRouter, Depends
from ..controllers import seller
from ..utils.auth import seller_required

router = APIRouter(prefix="/seller", tags=["Seller"])

@router.get("/dashboard")
async def get_seller_dashboard_stats(
    payload: dict = Depends(seller_required)
):
    return await seller.get_seller_dashboard_stats(payload["sub"])
