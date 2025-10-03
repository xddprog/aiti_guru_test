from app.core.dto.client import ClientModel, ClientWithOrders, ClientCreate, ClientUpdate
from app.core.services.base import BaseDbModelService
from app.core.repositories.client_repository import ClientRepository
from app.infrastructure.database.models.client import Client
from app.infrastructure.errors.client_errors import ClientNotFound


class ClientService(BaseDbModelService[Client]):
    repository: ClientRepository

    async def get_all_clients(self, limit: int, offset: int) -> list[ClientModel]:
        clients = await self.repository.get_all_items(limit, offset)
        return [
            ClientModel.model_validate(client, from_attributes=True)
            for client in clients
        ]
    
    async def get_client(self, client_id: int) -> ClientModel:
        client = await self.repository.get_item(client_id)
        if not client:
            raise ClientNotFound
        return ClientModel.model_validate(client, from_attributes=True)
    
    async def get_client_with_orders(self, client_id: int) -> ClientWithOrders:
        client = await self.repository.get_client_with_orders(client_id)
        if not client:
            raise ClientNotFound
        return ClientWithOrders.model_validate(client, from_attributes=True)
    
    async def get_client_by_name(self, name: str) -> ClientModel:
        client = await self.repository.get_client_by_name(name)
        if not client:
            raise ClientNotFound
        return ClientModel.model_validate(client, from_attributes=True)
    
    async def get_clients_filtered(self, limit: int, offset: int, name: str | None = None) -> list[ClientModel]:
        clients = await self.repository.get_clients_filtered(limit, offset, name)
        return [
            ClientModel.model_validate(client, from_attributes=True)
            for client in clients
        ]
    
    async def create_client(self, client_data: ClientCreate) -> ClientModel:
        create_data = client_data.model_dump()
        client = await self.repository.add_item(**create_data)
        return ClientModel.model_validate(client, from_attributes=True)
    
    async def update_client(self, client_id: int, client_data: ClientUpdate) -> ClientModel:
        update_data = client_data.model_dump(exclude_unset=True)
        client = await self.repository.update_item(client_id, **update_data)
        return ClientModel.model_validate(client, from_attributes=True)
