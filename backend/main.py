from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from contextlib import asynccontextmanager

from backend.utils.database import Database
from backend.utils.logger import logger
from backend.routes import auth, product, order, admin, seller, dialogflow

# Define lifespan context manager
@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup event - connect to database
    await Database.connect_db()
    yield
    # Shutdown event - close database connection
    await Database.close_db()

# Create FastAPI app with lifespan
app = FastAPI(
    title="E-commerce API",
    description="API cho ứng dụng bán hàng sử dụng FastAPI và MongoDB",
    version="1.0.0",
    lifespan=lifespan
)

# Phục vụ file tĩnh
app.mount("/static", StaticFiles(directory="static"), name="static")

# Cấu hình templates
templates = Jinja2Templates(directory="templates")

# Add CORS middleware
origins = ["*"]  # In production, replace with specific origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(_: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Đã xảy ra lỗi hệ thống"}
    )

# Include routers
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(admin.router)
app.include_router(seller.router)
app.include_router(dialogflow.router)

# Root endpoint - Frontend landing page
@app.get("/", tags=["Frontend"], response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

# Search page endpoint
@app.get("/search", tags=["Frontend"], response_class=HTMLResponse)
async def search_page(request: Request, q: str = None):
    return templates.TemplateResponse("search.html", {"request": request, "query": q})

# API root endpoint
@app.get("/api", tags=["API"])
async def read_root():
    return {
        "message": "Chào mừng đến với API E-commerce",
        "docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)