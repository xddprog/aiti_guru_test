from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from app.core.dto.client import ClientModel
from app.core.dto.product import ProductModel


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.core.dto.client import ClientModel


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemModel(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float



class OrderItemWithProduct(OrderItemModel):
    product: ProductModel



class OrderBase(BaseModel):
    client_id: int


class OrderCreate(OrderBase):
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderModel(BaseModel):
    id: int
    client_id: int
    created_at: datetime



class OrderWithDetails(OrderModel):
    client: ClientModel
    items: list[OrderItemWithProduct] = []



class OrderSummary(BaseModel):
    client_name: str
    total_amount: float


class AddItemToOrderRequest(BaseModel):
    product_id: int
    quantity: int


OrderWithDetails.model_rebuild()