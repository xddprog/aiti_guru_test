from pydantic import BaseModel


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.core.dto.order import OrderModel



class ClientBase(BaseModel):
    name: str
    address: str


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: str | None = None
    address: str | None = None


class ClientModel(BaseModel):
    id: int
    name: str
    address: str



class ClientWithOrders(ClientModel):
    orders: list["OrderModel"] = []



from app.core.dto.order import OrderModel
ClientWithOrders.model_rebuild()