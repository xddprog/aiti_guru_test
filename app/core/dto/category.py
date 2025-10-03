from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    parent_id: int | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    parent_id: int | None = None


class CategoryModel(BaseModel):
    id: int
    name: str
    parent_id: int | None = None



class CategoryWithChildren(CategoryModel):
    children: list["CategoryWithChildren"] = []



# Для избежания циклических ссылок
CategoryWithChildren.model_rebuild()