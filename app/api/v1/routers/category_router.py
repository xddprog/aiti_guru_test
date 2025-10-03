from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.api.v1.dependencies import get_category_service, get_product_service
from app.core.dto.category import CategoryModel, CategoryCreate, CategoryUpdate, CategoryWithChildren
from app.core.services.category_service import CategoryService


router = APIRouter()


@router.get("/", response_model=list[CategoryModel])
async def get_all_categories(
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    limit: int = 10,
    offset: int = 0
):
    return await category_service.get_all_categories(limit, offset)


@router.get("/tree", response_model=list[CategoryWithChildren])
async def get_category_tree(
    category_service: Annotated[CategoryService, Depends(get_category_service)]
):
    return await category_service.get_category_tree()


@router.get("/{category_id}", response_model=CategoryModel)
async def get_category(
    category_id: int,
    category_service: Annotated[CategoryService, Depends(get_category_service)]
):
    return await category_service.get_category(category_id)


@router.post("/", response_model=CategoryModel, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    category_service: Annotated[CategoryService, Depends(get_category_service)]
):
    return await category_service.create_category(category_data)


@router.put("/{category_id}", response_model=CategoryModel)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    return await category_service.update_category(category_id, category_data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    category_service: Annotated[CategoryService, Depends(get_category_service)]
):
    await category_service.delete_category(category_id)
