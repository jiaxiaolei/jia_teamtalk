import sys
import os
import logging
import argparse
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

# 1. 路径注入 (保持不变)
current_file_path = os.path.abspath(__file__)
app_dir = os.path.dirname(current_file_path)
src_dir = os.path.dirname(app_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# 2. 导入配置
from app.core.logger import configure_logging, LOGGING_CONFIG
from app.schemas.request import TranslationRequest
from app.adapters.qwen import QwenClient
from app.services.chat_service import ChatService

# 3. 先手动配置一次，确保在 app 启动前的日志也能生效
configure_logging()
#logger = logging.getLogger(__name__)

app = FastAPI(title="Enterprise AI Translator")

static_dir = os.path.join(os.path.dirname(src_dir), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    #logger.info(f"Static files mounted at: {static_dir}")
    logging.info(f"Static files mounted at: {static_dir}")
else:
    #logger.warning(f"Static directory not found at {static_dir}")
    logging.warning(f"Static directory not found at {static_dir}")

def get_chat_service():
    client = QwenClient() 
    return ChatService(client)

@app.post("/api/translate")
async def translate_endpoint(request: TranslationRequest, service: ChatService = Depends(get_chat_service)):
    stream_generator = await service.translate(request.direction, request.content)
    return StreamingResponse(stream_generator, media_type="text/event-stream")

if __name__ == "__main__":

    # 1. 定义参数解析器
    parser = argparse.ArgumentParser(description="职能沟通翻译助手启动程序")

    # 2. 定义命令行参数 (模仿 tornado.options.define)
    # type=int: 自动把输入转成整数
    # default=8081: 如果不传，默认用 8081
    # help: 帮助说明
    parser.add_argument("--port", type=int, default=8081, help="监听端口 (默认: 8081)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="绑定地址 (默认: 0.0.0.0)")
    parser.add_argument("--reload", action="store_true", help="是否开启热重载 (开发模式)")

    # 3. 解析参数
    args = parser.parse_args()

    # 4. 打印启动信息
    #logger.info(f"🚀 logger Server is starting on http://{args.host}:{args.port}")
    logging.info(f"🚀 logging Server is starting on http://{args.host}:{args.port}")
    if args.reload:
        logger.warning("⚠️  Hot reload is enabled (Development Mode)")

    # 5. 启动 Uvicorn，使用解析出来的 args.host 和 args.port
    # =======================================================
    # 🔑 关键修改：将 log_config 传给 uvicorn
    # 这样 Uvicorn 就会使用我们定义的 TornadoLogFormatter
    # =======================================================
    uvicorn.run(
        "app.main:app" if args.reload else app, # 热重载模式需传字符串
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_config=LOGGING_CONFIG # 保持日志配置
    )

