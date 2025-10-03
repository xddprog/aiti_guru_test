from fastapi import HTTPException


class CategoryNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Category not found")


class CategoryHasChildren(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Cannot delete category with children")


class InvalidParentCategory(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid parent category")
