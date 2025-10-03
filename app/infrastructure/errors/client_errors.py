from fastapi import HTTPException


class ClientNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Client not found")


class ClientAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Client with this name already exists")
