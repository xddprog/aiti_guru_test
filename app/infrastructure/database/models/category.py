from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.infrastructure.database.models.product import Product



class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    
    parent: Mapped["Category | None"] = relationship(
        "Category", 
        remote_side=[id],
        back_populates="children"
    )
    children: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="parent",
        cascade="all, delete-orphan",
        lazy="selectin",
        join_depth=10
    )
    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category"
    )

