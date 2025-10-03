from fastapi import HTTPException


class OrderNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Order not found")


class OrderItemNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Order item not found")


class InvalidOrderData(HTTPException):
    def __init__(self, message: str = "Invalid order data"):
        super().__init__(status_code=400, detail=message)


class EmptyOrder(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Order must contain at least one item")
