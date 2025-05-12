from fastapi import HTTPException, status
from bson.objectid import ObjectId
from datetime import datetime, UTC
from typing import List, Optional

from ..models.product import ProductCreate, ProductUpdate, ProductInDB, ReviewCreate, ReviewInDB, ReportCreate,ReportInDB, PyObjectId
from ..utils.database import Database
from ..utils.logger import logger


async def search_products(
        query: str,
        limit: int = 10,
        skip: int = 0,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None
):
    filter_query = {
        "$text": {"$search": query}
    }

    # Thêm bộ lọc theo danh mục nếu có
    if category:
        filter_query["category"] = category

    # Thêm bộ lọc theo giá nếu có
    if min_price is not None or max_price is not None:
        price_filter = {}
        if min_price is not None:
            price_filter["$gte"] = min_price
        if max_price is not None:
            price_filter["$lte"] = max_price
        if price_filter:
            filter_query["price"] = price_filter

    # Thêm bộ lọc theo đánh giá nếu có
    if min_rating is not None:
        filter_query["avg_rating"] = {"$gte": min_rating}

    # Tìm kiếm sản phẩm và sắp xếp theo điểm liên quan
    products = await db.products.find(
        filter_query,
        {"score": {"$meta": "textScore"}}
    ).sort(
        [("score", {"$meta": "textScore"})]
    ).skip(skip).limit(limit).to_list(length=limit)

    # Nếu không tìm thấy kết quả với text search, thử tìm theo regex
    if not products:
        regex_query = {
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        }

        # Thêm lại các bộ lọc
        if category:
            regex_query["category"] = category

        if min_price is not None or max_price is not None:
            price_filter = {}
            if min_price is not None:
                price_filter["$gte"] = min_price
            if max_price is not None:
                price_filter["$lte"] = max_price
            if price_filter:
                regex_query["price"] = price_filter

        if min_rating is not None:
            regex_query["avg_rating"] = {"$gte": min_rating}

        products = await db.products.find(regex_query).skip(skip).limit(limit).to_list(length=limit)

    # Chuyển đổi ObjectId thành chuỗi
    for product in products:
        product["_id"] = str(product["_id"])
        if "seller_id" in product:
            product["seller_id"] = str(product["seller_id"])

    return products

async def create_product(product: ProductCreate, seller_id: str):
    # Create product document
    product_data = ProductInDB(
        **product.model_dump(),
        seller_id=PyObjectId(seller_id),
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )

    # Insert product into database
    result = await Database.db.products.insert_one(product_data.model_dump(by_alias=True))

    # Get created product
    created_product = await Database.db.products.find_one({"_id": result.inserted_id})

    logger.info(f"Product created: {product.name} by seller {seller_id}")

    # Convert ObjectId to string
    created_product["_id"] = str(created_product["_id"])
    created_product["seller_id"] = str(created_product["seller_id"])

    return created_product


async def get_all_products(limit: int = 10, skip: int = 0, category: Optional[str] = None,
                           search: Optional[str] = None, sort_by: Optional[str] = None):
    # Build query
    query = {}
    if category:
        query["category"] = category
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]

    # Build sort
    sort_dict = {}
    if sort_by:
        if sort_by == "price_asc":
            sort_dict["price"] = 1
        elif sort_by == "price_desc":
            sort_dict["price"] = -1
        elif sort_by == "newest":
            sort_dict["created_at"] = -1
    else:
        sort_dict["created_at"] = -1

    # Query database
    cursor = Database.db.products.find(query).sort(list(sort_dict.items())).skip(skip).limit(limit)
    products = await cursor.to_list(length=limit)

    # Convert ObjectId to string
    for product in products:
        product["_id"] = str(product["_id"])
        product["seller_id"] = str(product["seller_id"])

    return products


async def get_product_by_id(product_id: str):
    try:
        # Find product by id
        product = await Database.db.products.find_one({"_id": ObjectId(product_id)})

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sản phẩm không tồn tại",
            )

        # Convert ObjectId to string
        product["_id"] = str(product["_id"])
        product["seller_id"] = str(product["seller_id"])

        return product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ID sản phẩm không hợp lệ: {str(e)}",
        )


async def update_product(product_id: str, product_update: ProductUpdate, seller_id: str):
    try:
        # Find product by id
        product = await Database.db.products.find_one({"_id": ObjectId(product_id)})

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sản phẩm không tồn tại",
            )

        # Check if user is the seller
        if str(product["seller_id"]) != seller_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền cập nhật sản phẩm này",
            )

        # Update product
        update_data = {k: v for k, v in product_update.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.now(UTC)

        await Database.db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )

        # Get updated product
        updated_product = await Database.db.products.find_one({"_id": ObjectId(product_id)})

        logger.info(f"Product updated: {product_id} by seller {seller_id}")

        # Convert ObjectId to string
        updated_product["_id"] = str(updated_product["_id"])
        updated_product["seller_id"] = str(updated_product["seller_id"])

        return updated_product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ID sản phẩm không hợp lệ: {str(e)}",
        )


async def delete_product(product_id: str, user_id: str, is_admin: bool = False):
    try:
        # Find product by id
        product = await Database.db.products.find_one({"_id": ObjectId(product_id)})

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sản phẩm không tồn tại",
            )

        # Check if user is the seller or admin
        if str(product["seller_id"]) != user_id and not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền xóa sản phẩm này",
            )

        # Delete product
        await Database.db.products.delete_one({"_id": ObjectId(product_id)})

        logger.info(f"Product deleted: {product_id} by user {user_id}")

        return {"message": "Sản phẩm đã được xóa thành công"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ID sản phẩm không hợp lệ: {str(e)}",
        )


async def get_seller_products(seller_id: str):
    # Find products by seller_id
    cursor = Database.db.products.find({"seller_id": ObjectId(seller_id)}).sort("created_at", -1)
    products = await cursor.to_list(length=100)

    # Convert ObjectId to string
    for product in products:
        product["_id"] = str(product["_id"])
        product["seller_id"] = str(product["seller_id"])

    return products


async def create_review(review: ReviewCreate, user_id: str):
    try:
        # Check if product exists
        product = await Database.db.products.find_one({"_id": ObjectId(review.product_id)})

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sản phẩm không tồn tại",
            )

        # Check if user already reviewed this product
        existing_review = await Database.db.reviews.find_one({
            "product_id": review.product_id,
            "user_id": ObjectId(user_id)
        })

        if existing_review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bạn đã đánh giá sản phẩm này rồi",
            )

        # Create review document
        review_data = ReviewInDB(
            **review.model_dump(),
            user_id=PyObjectId(user_id),
            created_at=datetime.now(UTC)
        )

        # Insert review into database
        result = await Database.db.reviews.insert_one(review_data.model_dump(by_alias=True))

        # Get created review
        created_review = await Database.db.reviews.find_one({"_id": result.inserted_id})

        logger.info(f"Review created for product {review.product_id} by user {user_id}")

        # Convert ObjectId to string
        created_review["_id"] = str(created_review["_id"])
        created_review["user_id"] = str(created_review["user_id"])

        return created_review
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lỗi khi tạo đánh giá: {str(e)}",
        )


async def get_product_reviews(product_id: str):
    try:
        # Find reviews by product_id
        cursor = Database.db.reviews.find({"product_id": product_id}).sort("created_at", -1)
        reviews = await cursor.to_list(length=100)

        # Convert ObjectId to string
        for review in reviews:
            review["_id"] = str(review["_id"])
            review["user_id"] = str(review["user_id"])

        return reviews
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ID sản phẩm không hợp lệ: {str(e)}",
        )


async def create_report(report: ReportCreate, user_id: str):
    try:
        # Check if product exists
        product = await Database.db.products.find_one({"_id": ObjectId(report.product_id)})

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sản phẩm không tồn tại",
            )

        # Create report document
        report_data = ReportInDB(
            **report.model_dump(),
            user_id=PyObjectId(user_id),
            created_at=datetime.now(UTC)
        )

        # Insert report into database
        result = await Database.db.reports.insert_one(report_data.model_dump(by_alias=True))

        # Get created report
        created_report = await Database.db.reports.find_one({"_id": result.inserted_id})

        logger.info(f"Report created for product {report.product_id} by user {user_id}")

        # Convert ObjectId to string
        created_report["_id"] = str(created_report["_id"])
        created_report["user_id"] = str(created_report["user_id"])

        return created_report
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lỗi khi tạo báo cáo: {str(e)}",
        )