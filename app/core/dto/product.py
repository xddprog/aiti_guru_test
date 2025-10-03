from decimal import Decimal
from pydantic import BaseModel
from app.core.dto.category import CategoryModel


class ProductBase(BaseModel):
    name: str
    category_id: int
    price: Decimal


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    category_id: int | None = None
    price: Decimal | None = None



class ProductModel(BaseModel):
    id: int
    name: str
    category_id: int
    price: float



class ProductWithCategory(ProductModel):
    category: CategoryModel

