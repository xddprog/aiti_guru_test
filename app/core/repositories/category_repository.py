from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.repositories.base import SqlAlchemyRepository
from app.infrastructure.database.models.category import Category


class CategoryRepository(SqlAlchemyRepository[Category]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Category)
    
    async def get_root_categories(self) -> list[Category]:
        query = select(Category).where(Category.parent_id.is_(None))
        result = await self.session.execute(query)
        return result.scalars().unique().all()
    
    async def get_category_with_children(self, category_id: int) -> Category | None:
        query = (
            select(Category)
            .options(selectinload(Category.children))
            .where(Category.id == category_id)
        )
        result = await self.session.execute(query)
        return result.scalars().unique().first()
    
    async def get_category_tree(self) -> list[Category]:
        query = (
            select(Category)
            .options(selectinload(Category.children))
            .where(Category.parent_id.is_(None))
        )
        result = await self.session.execute(query)
        return result.scalars().unique().all()
