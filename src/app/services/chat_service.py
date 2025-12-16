
import logging

from app.adapters.base import BaseLLMClient
from app.strategies.factory import RoleFactory

class ChatService:
    def __init__(self, llm_client: BaseLLMClient):
        # 依赖注入 LLM 客户端
        self.llm = llm_client

    async def translate(self, role_type: str, content: str):
        # 1. 获取对应角色的策略
        strategy = RoleFactory.get_strategy(role_type)

        # 2. 构建符合 OpenAI 格式的消息体
        messages = [
            {"role": "system", "content": strategy.system_prompt},
            {"role": "user", "content": strategy.build_user_prompt(content)}
        ]
        logging.info("[ChatService] messages: %s", messages)

        # 3. 调用 LLM 并返回生成器
        return self.llm.stream_chat(messages)
