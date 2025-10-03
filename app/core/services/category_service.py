from sqlalchemy.exc import IntegrityError
from app.core.dto.category import CategoryModel, CategoryWithChildren, CategoryCreate, CategoryUpdate
from app.core.services.base import BaseDbModelService
from app.core.repositories.category_repository import CategoryRepository
from app.infrastructure.database.models.category import Category
from app.infrastructure.errors.category_errors import CategoryHasChildren, CategoryNotFound


class CategoryService(BaseDbModelService[Category]):
    repository: CategoryRepository

    async def get_all_categories(self, limit: int, offset: int) -> list[CategoryModel]:
        categories = await self.repository.get_all_items(limit, offset)
        return [
            CategoryModel.model_validate(category, from_attributes=True)
            for category in categories
        ]
    
    async def get_category(self, category_id: int) -> CategoryWithChildren:
        category = await self.repository.get_category_with_children(category_id)
        if not category:
            raise CategoryNotFound
        return CategoryWithChildren.model_validate(category, from_attributes=True)
    
    async def get_root_categories(self) -> list[CategoryModel]:
        categories = await self.repository.get_root_categories()
        return [
            CategoryModel.model_validate(category, from_attributes=True)
            for category in categories
        ]
    
    async def get_category_tree(self) -> list[CategoryWithChildren]:
        categories = await self.repository.get_category_tree()
        return [
            CategoryWithChildren.model_validate(category, from_attributes=True)
            for category in categories
        ]
    
    async def create_category(self, category_data: CategoryCreate) -> CategoryModel:
        create_data = category_data.model_dump()
        category = await self.repository.add_item(**create_data)
        return CategoryModel.model_validate(category, from_attributes=True)
    
    async def update_category(self, category_id: int, category_data: CategoryUpdate) -> CategoryModel:
        update_data = category_data.model_dump(exclude_unset=True)
        category = await self.repository.update_item(category_id, **update_data)
        return CategoryModel.model_validate(category, from_attributes=True)
    
    async def delete_category(self, category_id: int) -> None:
        category = await self.repository.get_item(category_id)
        if not category:
            raise CategoryNotFound
        try:
            await self.repository.delete_item(category)
        except IntegrityError:
            raise CategoryHasChildren
