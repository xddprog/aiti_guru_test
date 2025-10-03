from app.core.dto.product import ProductModel, ProductWithCategory, ProductCreate, ProductUpdate
from app.core.services.base import BaseDbModelService
from app.core.repositories.product_repository import ProductRepository
from app.infrastructure.database.models.product import Product
from app.infrastructure.errors.product_errors import ProductNotFound


class ProductService(BaseDbModelService[Product]):
    repository: ProductRepository

    async def get_all_products(self, limit: int, offset: int) -> list[ProductModel]:
        products = await self.repository.get_all_items(limit, offset)
        return [
            ProductModel.model_validate(product, from_attributes=True)
            for product in products
        ]
    
    async def get_product(self, product_id: int) -> ProductWithCategory:
        product = await self.repository.get_product_with_category(product_id)
        if not product:
            raise ProductNotFound
        return ProductWithCategory.model_validate(product, from_attributes=True)
    
    async def get_products_filtered(
        self, 
        limit: int,
        offset: int,
        category_id: int | None = None, 
        name: str | None = None
    ) -> list[ProductWithCategory]:
        products = await self.repository.get_products_filtered(limit, offset, category_id, name)
        return [
            ProductWithCategory.model_validate(product, from_attributes=True)
            for product in products
        ]
    
    async def create_product(self, product_data: ProductCreate) -> ProductModel:
        product = await self.repository.add_item(**product_data.model_dump())
        return ProductModel.model_validate(product, from_attributes=True)
    
    async def update_product(self, product_id: int, product_data: ProductUpdate) -> ProductModel:
        product = await self.repository.update_item(product_id, **product_data.model_dump(exclude_unset=True))
        return ProductModel.model_validate(product, from_attributes=True)