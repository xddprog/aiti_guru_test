from typing import Any
from app.infrastructure.interfaces.repository import RepositoryInterface

class BaseDbModelService[ModelType]:
    def __init__(
        self, repository: RepositoryInterface[ModelType],
    ):
        self.repository = repository
