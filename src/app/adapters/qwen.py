import logging

from openai import AsyncOpenAI
from app.core.config import settings
from app.adapters.base import BaseLLMClient

#logger = logging.getLogger(__name__)

class QwenClient(BaseLLMClient):
    def __init__(self):
        # 初始化 OpenAI 客户端但指向阿里服务
        self.client = AsyncOpenAI(
            api_key=settings.DASHSCOPE_API_KEY,
            base_url=settings.BASE_URL
        )

    async def stream_chat(self, messages: list):
        try:
            response = await self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=messages,
                stream=True,
                temperature=0.7
            )
            async for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

            logging.info(f"Calling Qwen Model with {len(messages)} messages") # 记录调用信息
        except Exception as e:
            #logging.error(f"---loggingLLM API Call Failed: {str(e)}", exc_info=True) # 记录错误堆栈
            logging.exception(f"---loggingLLM API Call Failed: {str(e)}", exc_info=True) # 记录错误堆栈
            #logger.error(f"---logger LLM API Call Failed: {str(e)}", exc_info=True)
            logger.exception(f"---logger LLM API Call Failed: {str(e)}", exc_info=True)
            yield f"[System Error]: LLM调用失败 - {str(e)}"

