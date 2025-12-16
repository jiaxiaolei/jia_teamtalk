from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DASHSCOPE_API_KEY: str
    MODEL_NAME: str = "qwen-turbo"
    # 使用兼容协议的 Base URL，这是架构设计的亮点：解耦
    BASE_URL: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    class Config:
        env_file = ".env"

settings = Settings()
