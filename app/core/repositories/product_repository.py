from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.repositories.base import SqlAlchemyRepository
from app.infrastructure.database.models.product import Product


class ProductRepository(SqlAlchemyRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Product)
    
    async def get_products_filtered(
        self, 
        limit: int,
        offset: int,
        category_id: int | None = None, 
        name: str | None = None
    ) -> list[Product]:
        query = select(Product).options(selectinload(Product.category))
        
        if category_id:
            query = query.where(Product.category_id == category_id)
        if name:
            query = query.where(Product.name.ilike(f"%{name}%"))
            
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_product_with_category(self, product_id: int) -> Product | None:
        query = (
            select(Product)
            .options(selectinload(Product.category))
            .where(Product.id == product_id)
        )
        result = await self.session.execute(query)
        return result.scalars().first()
