from pydantic import BaseModel, Field
from typing import Literal

# 定义枚举类型，限制输入范围
RoleType = Literal["p2d", "d2p"]

class TranslationRequest(BaseModel):
    direction: RoleType = Field(..., description="翻译方向: p2d(产品转开发) 或 d2p(开发转产品)")
    content: str = Field(..., min_length=5, max_length=2000, description="需要翻译的原始内容")
