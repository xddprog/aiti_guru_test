from fastapi import APIRouter

from app.api.v1.routers.category_router import router as category_router
from app.api.v1.routers.product_router import router as product_router
from app.api.v1.routers.client_router import router as client_router
from app.api.v1.routers.order_router import router as order_router


all_routers = APIRouter(prefix="/api/v1")

all_routers.include_router(
    category_router, 
    tags=["CATEGORY"], 
    prefix="/category"
)
all_routers.include_router(
    product_router, 
    tags=["PRODUCT"], 
    prefix="/product"
)
all_routers.include_router(
    client_router, 
    tags=["CLIENT"], 
    prefix="/client"
)
all_routers.include_router(
    order_router, 
    tags=["ORDER"], 
    prefix="/order"
)
