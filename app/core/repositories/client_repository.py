from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.repositories.base import SqlAlchemyRepository
from app.infrastructure.database.models.client import Client


class ClientRepository(SqlAlchemyRepository[Client]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Client)
    
    async def get_client_by_name(self, name: str) -> Client | None:
        query = select(Client).where(Client.name == name)
        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def get_clients_filtered(
        self, 
        limit: int,
        offset: int,
        name: str | None = None,
    ) -> list[Client]:
        query = select(Client)
        
        if name:
            query = query.where(Client.name.ilike(f"%{name}%"))
            
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_client_with_orders(self, client_id: int) -> Client | None:
        query = (
            select(Client)
            .options(selectinload(Client.orders))
            .where(Client.id == client_id)
        )
        result = await self.session.execute(query)
        return result.scalars().first()
