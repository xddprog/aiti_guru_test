from datetime import datetime
from decimal import Decimal
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.infrastructure.database.models.base import Base


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.infrastructure.database.models.client import Client
    from app.infrastructure.database.models.product import Product



class Order(Base):
    __tablename__ = "orders"

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    
    client: Mapped["Client"] = relationship(
        "Client",
        back_populates="orders",
        lazy="selectin"
    )
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]
    price: Mapped[Decimal]
    
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="items"
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="order_items",
        lazy="selectin"
    )

