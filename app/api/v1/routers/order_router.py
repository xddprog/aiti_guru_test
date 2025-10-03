from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Depends, status

from app.api.v1.dependencies import get_order_service
from app.core.dto.order import (
    OrderModel, OrderCreate, OrderWithDetails, 
    AddItemToOrderRequest, OrderItemModel, OrderSummary
)
from app.core.services.order_service import OrderService


router = APIRouter()


@router.get("/", response_model=list[OrderWithDetails])
async def get_orders(
    order_service: Annotated[OrderService, Depends(get_order_service)],
    client_id: int | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    limit: int = 10,
    offset: int = 0,
):
    return await order_service.get_orders_filtered(
        limit=limit,
        offset=offset,
        client_id=client_id,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/client-totals", response_model=list[OrderSummary])
async def get_client_order_totals(
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    return await order_service.get_client_order_totals()


@router.get("/{order_id}", response_model=OrderWithDetails)
async def get_order(
    order_id: int,
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    return await order_service.get_order(order_id)


@router.post("/", response_model=OrderWithDetails, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    client_id: int,
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    return await order_service.create_order(client_id, order_data)


@router.delete("/{order_id}", )
async def delete_order(
    order_id: int,
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    await order_service.delete_order(order_id)


@router.post("/{order_id}/items", response_model=OrderItemModel)
async def add_item_to_order(
    order_id: int,
    item_data: AddItemToOrderRequest,
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    return await order_service.add_item_to_order(
        order_id=order_id,
        product_id=item_data.product_id,
        quantity=item_data.quantity
    )


@router.put("/{order_id}/items/{order_item_id}", response_model=OrderItemModel)
async def update_order_item_quantity(
    order_id: int,
    order_item_id: int,
    quantity: int,
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    return await order_service.update_order_item_quantity(order_id, order_item_id, quantity)


@router.delete("/{order_id}/items/{order_item_id}")
async def remove_item_from_order(
    order_id: int,
    order_item_id: int,
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    await order_service.remove_item_from_order(order_id, order_item_id)