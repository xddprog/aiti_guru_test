from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.dependencies import get_client_service
from app.core.dto.client import ClientModel, ClientCreate, ClientUpdate, ClientWithOrders
from app.core.services.client_service import ClientService


router = APIRouter()


@router.get("/", response_model=list[ClientModel])
async def get_clients(
    client_service: Annotated[ClientService, Depends(get_client_service)],
    limit: int = 10,
    offset: int = 0,
    name: str | None = None,
):
    return await client_service.get_clients_filtered(
        limit=limit, 
        offset=offset,
        name=name
    )


@router.get("/{client_id}", response_model=ClientModel)
async def get_client(
    client_id: int,
    client_service: Annotated[ClientService, Depends(get_client_service)]
):
    return await client_service.get_client(client_id)


@router.post("/", response_model=ClientModel, status_code=status.HTTP_201_CREATED)
async def create_client(
    client_data: ClientCreate,
    client_service: Annotated[ClientService, Depends(get_client_service)]
):
    return await client_service.create_client(client_data)


@router.put("/{client_id}", response_model=ClientModel)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    client_service: Annotated[ClientService, Depends(get_client_service)]
):
    return await client_service.update_client(client_id, client_data)
