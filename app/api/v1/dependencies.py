from typing import AsyncGenerator
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.services import CategoryService, ProductService, ClientService, OrderService
from app.core.repositories import CategoryRepository, ProductRepository, ClientRepository, OrderRepository, OrderItemRepository


async def get_db_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    session = await request.app.state.db_connection.get_session()
    try:
        yield session
    finally:
        await session.close()


async def get_category_service(session=Depends(get_db_session)) -> CategoryService:
    return CategoryService(
        repository=CategoryRepository(session=session)
    )


async def get_product_service(session=Depends(get_db_session)) -> ProductService:
    return ProductService(
        repository=ProductRepository(session=session)
    )


async def get_client_service(session=Depends(get_db_session)) -> ClientService:
    return ClientService(
        repository=ClientRepository(session=session)
    )


async def get_order_service(session=Depends(get_db_session)) -> OrderService:
    return OrderService(
        repository=OrderRepository(session=session),
        order_item_repository=OrderItemRepository(session=session),
        product_repository=ProductRepository(session=session)
    )