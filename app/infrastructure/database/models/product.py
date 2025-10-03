from decimal import Decimal
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models.base import Base


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.infrastructure.database.models.category import Category
    from app.infrastructure.database.models.order import OrderItem


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    price: Mapped[Decimal]
    
    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products",
        lazy="selectin"
    )
    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="product"
    )

