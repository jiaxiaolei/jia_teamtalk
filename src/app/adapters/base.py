from abc import ABC, abstractmethod
from typing import AsyncGenerator

class BaseLLMClient(ABC):
    @abstractmethod
    async def stream_chat(self, messages: list) -> AsyncGenerator[str, None]:
        """流式对话接口"""
        pass
