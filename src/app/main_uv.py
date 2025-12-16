import sys
import os
import uvicorn
import logging

from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

# --- 核心修复：路径注入 ---
# 获取当前文件 (main.py) 的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取 app 目录路径 (.../src/app)
app_dir = os.path.dirname(current_file_path)
# 获取 src 目录路径 (.../src)
src_dir = os.path.dirname(app_dir)

# 将 src 目录加入到 Python 的搜索路径中
# 这样 Python 才能找到 "app" 这个包
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
# -----------------------

# 路径注入后，才能正常 import app.xxx
from app.core.logger import configure_logging
from app.schemas.request import TranslationRequest
from app.adapters.qwen import QwenClient
from app.services.chat_service import ChatService

#获取当前模块的 logger (推荐写法)
# 这样日志里会显示 "app.main"，而不是 generic 的 root
logger = logging.getLogger(__name__)
app = FastAPI(title="Enterprise AI Translator")

# 挂载静态文件
# 注意：这里使用 os.path.join 确保在任何目录下运行都能找到 static 目录
static_dir = os.path.join(os.path.dirname(src_dir), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    logger.info(f"Static files mounted at: {static_dir}")
else:
    logger.warning(f"Static directory not found at {static_dir}") 

def get_chat_service():
    client = QwenClient()
    return ChatService(client)

@app.post("/api/translate")
async def translate_endpoint(
    request: TranslationRequest,
    service: ChatService = Depends(get_chat_service)
):
    stream_generator = await service.translate(request.direction, request.content)
    return StreamingResponse(stream_generator, media_type="text/event-stream")

if __name__ == "__main__":
    # 方式 A：直接运行脚本时的启动逻辑
    # 注意：直接传 app 对象，而不是字符串 "app.main:app"，避免路径解析麻烦
    # reload=False 是因为直接运行脚本通常用于生产或调试，不需要热重载
    # 如果一定需要 reload，必须确保环境变量 PYTHONPATH 包含 src
    logger.info("🚀 Server is starting on http://0.0.0.0:8001")
    uvicorn.run(app, host="0.0.0.0", port=8002)
