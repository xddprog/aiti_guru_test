from datetime import datetime
from app.core.dto.order import OrderModel, OrderWithDetails, OrderItemModel, OrderSummary, OrderCreate
from app.core.services.base import BaseDbModelService
from app.core.repositories.order_repository import OrderRepository, OrderItemRepository
from app.core.repositories.product_repository import ProductRepository
from app.infrastructure.database.models.order import Order
from app.infrastructure.errors.order_errors import OrderNotFound, OrderItemNotFound, InvalidOrderData, EmptyOrder
from app.infrastructure.errors.product_errors import ProductNotFound


class OrderService(BaseDbModelService[Order]):
    def __init__(
        self, 
        repository: OrderRepository, 
        order_item_repository: OrderItemRepository,
        product_repository: ProductRepository
    ):
        super().__init__(repository)
        self.repository = repository
        self.order_item_repository = order_item_repository
        self.product_repository = product_repository
    
    async def get_all_orders(self, limit: int = 10, offset: int = 0) -> list[OrderModel]:
        orders = await self.repository.get_all_items(limit=limit, offset=offset)
        return [
            OrderModel.model_validate(order, from_attributes=True)
            for order in orders
        ]
    
    async def get_order(self, order_id: int) -> OrderWithDetails:

        order = await self.repository.get_order_with_items(order_id)
        if not order:
            raise OrderNotFound
        return OrderWithDetails.model_validate(order, from_attributes=True)
    
    async def get_orders_filtered(
        self,
        limit: int,
        offset: int,
        client_id: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None
    ) -> list[OrderWithDetails]:
        orders = await self.repository.get_orders_filtered(limit, offset, client_id, start_date, end_date)
        return [
            OrderWithDetails.model_validate(order, from_attributes=True)
            for order in orders
        ]
    
    async def get_client_order_totals(self) -> list[OrderSummary]:
        totals = await self.repository.get_client_order_totals()
        return [
            OrderSummary(client_name=client_name, total_amount=total)
            for client_name, total in totals
        ]
    
    async def create_order(self, client_id: int, form: OrderCreate) -> OrderWithDetails:
        if not form.items:
            raise EmptyOrder
            
        order = await self.repository.add_item(client_id=client_id)
        
        for item_data in form.items:
            product = await self.product_repository.get_item(item_data.product_id)
            if not product:
                raise ProductNotFound
            
            await self.order_item_repository.add_item(
                order_id=order.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                price=product.price
            )
        
        await self.repository.refresh(order)
        order_with_items = await self.repository.get_order_with_items(order.id)
        return OrderWithDetails.model_validate(order_with_items, from_attributes=True)
    
    async def add_item_to_order(self, order_id: int, product_id: int, quantity: int) -> OrderItemModel:
        order = await self.repository.get_item(order_id)
        if not order:
            raise OrderNotFound
            
        existing_items = await self.order_item_repository.get_items_by_order(order_id)
        existing_item = next((item for item in existing_items if item.product_id == product_id), None)
        
        if existing_item:
            updated_item = await self.order_item_repository.update_item(
                existing_item.id,
                quantity=existing_item.quantity + quantity
            )
            return OrderItemModel.model_validate(updated_item, from_attributes=True)
        else:
            product = await self.product_repository.get_item(product_id)
            if not product:
                raise ProductNotFound
            
            new_item = await self.order_item_repository.add_item(
                order_id=order_id,
                product_id=product_id,
                quantity=quantity,
                price=product.price
            )
            return OrderItemModel.model_validate(new_item, from_attributes=True)
    
    async def update_order_item_quantity(self, order_id: int, order_item_id: int, quantity: int) -> OrderItemModel:
        item = await self.order_item_repository.get_item_by_order_and_id(order_id, order_item_id)
        if not item:
            raise OrderItemNotFound
            
        updated_item = await self.order_item_repository.update_item(order_item_id, quantity=quantity)
        return OrderItemModel.model_validate(updated_item, from_attributes=True)
    
    async def remove_item_from_order(self, order_id: int, order_item_id: int) -> None:
        item = await self.order_item_repository.get_item_by_order_and_id(order_id, order_item_id)
        if not item:
            raise OrderItemNotFound
            
        await self.order_item_repository.delete_item(item)
    
    async def delete_order(self, order_id: int) -> None:
        order = await self.repository.get_item(order_id)
        if not order:
            raise OrderNotFound
        await self.repository.delete_item(order)
