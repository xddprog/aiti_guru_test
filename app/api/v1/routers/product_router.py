from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.api.v1.dependencies import get_product_service
from app.api.v1.dependencies import get_category_service
from app.core.dto.product import ProductModel, ProductCreate, ProductUpdate, ProductWithCategory
from app.core.services.category_service import CategoryService
from app.core.services.product_service import ProductService


router = APIRouter()


@router.get("/", response_model=list[ProductWithCategory])
async def get_products(
    product_service: Annotated[ProductService, Depends(get_product_service)],
    category_id: int | None = None,
    name: str | None = None,
    limit: int = 10,
    offset: int = 0
):
    return await product_service.get_products_filtered(
        limit=limit, 
        offset=offset,
        category_id=category_id, 
        name=name
    )


@router.get("/{product_id}", response_model=ProductWithCategory)
async def get_product(
    product_id: int,
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    return await product_service.get_product(product_id)


@router.post("/", response_model=ProductModel, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    product_service: Annotated[ProductService, Depends(get_product_service)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    await category_service.get_category(product_data.category_id)
    return await product_service.create_product(product_data)


@router.put("/{product_id}", response_model=ProductModel)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    product_service: Annotated[ProductService, Depends(get_product_service)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    
    category = await category_service.get_category(product_data.category_id)        
    if not category:
        product_data.category_id = None
    return await product_service.update_product(product_id, product_data)
