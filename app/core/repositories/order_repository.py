from datetime import datetime
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.repositories.base import SqlAlchemyRepository
from app.infrastructure.database.models.order import Order, OrderItem
from app.infrastructure.database.models.client import Client


class OrderRepository(SqlAlchemyRepository[Order]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Order)
    
    async def get_order_with_items(self, order_id: int) -> Order | None:
        query = (
            select(Order)
            .options(
                selectinload(Order.client),
                selectinload(Order.items).selectinload(OrderItem.product)
            )
            .where(Order.id == order_id)
        )
        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def get_orders_filtered(
        self,
        limit: int,
        offset: int,
        client_id: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None
    ) -> list[Order]:
        query = (
            select(Order)
            .options(
                selectinload(Order.client),
                selectinload(Order.items).selectinload(OrderItem.product)
            )
        )
        
        if client_id:
            query = query.where(Order.client_id == client_id)
        if start_date and end_date:
            query = query.where(Order.created_at.between(start_date, end_date))
            
        query = query.order_by(desc(Order.created_at)).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_client_order_totals(self) -> list[tuple[str, float]]:
        query = (
            select(
                Client.name,
                func.sum(OrderItem.price * OrderItem.quantity).label('total')
            )
            .join(Order, Client.id == Order.client_id)
            .join(OrderItem, Order.id == OrderItem.order_id)
            .group_by(Client.id, Client.name)
            .order_by(desc('total'))
        )
        result = await self.session.execute(query)
        return result.all()


class OrderItemRepository(SqlAlchemyRepository[OrderItem]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OrderItem)
    
    async def get_items_by_order(self, order_id: int) -> list[OrderItem]:
        query = (
            select(OrderItem)
            .options(selectinload(OrderItem.product))
            .where(OrderItem.order_id == order_id)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_item_by_order_and_id(self, order_id: int, item_id: int) -> OrderItem | None:
        query = (
            select(OrderItem)
            .where(OrderItem.id == item_id)
            .where(OrderItem.order_id == order_id)
        )
        result = await self.session.execute(query)
        return result.scalars().first()
