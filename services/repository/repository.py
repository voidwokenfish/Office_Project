from abc import ABC, abstractmethod
from typing import List
from services.models import BaseModel

class BaseRepository(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get(self, id: int):
        pass

    @abstractmethod
    def list(self) -> List[BaseModel]:
        pass

    @abstractmethod
    def add(self, entity: BaseModel) -> bool:
        pass

    @abstractmethod
    def update(self, entity: BaseModel) -> bool:
        pass

    @abstractmethod
    def delete(self, entity: BaseModel) -> bool:
        pass


