from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.database.models.base import Base


class Client(Base):
    __tablename__ = "clients"

    name: Mapped[str]
    address: Mapped[str]
    
   
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="client"
    )


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.infrastructure.database.models.order import Order
