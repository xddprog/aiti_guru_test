from fastapi import HTTPException


class ProductNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Product not found")


class InvalidCategory(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid category for product")


class ProductAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Product with this name already exists")
