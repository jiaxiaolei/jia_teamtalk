
from abc import ABC, abstractmethod

class BaseRoleStrategy(ABC):
    @property
    @abstractmethod
    def system_prompt(self) -> str:
        pass

    @abstractmethod
    def build_user_prompt(self, content: str) -> str:
        pass
