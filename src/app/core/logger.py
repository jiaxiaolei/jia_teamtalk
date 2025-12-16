import logging
import sys

# 定义日志格式：时间 - 级别 - 模块名 - 消息
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

def setup_logger(name: str = "app"):
    """
    配置并返回一个标准 Logger
    """
    logger = logging.getLogger(name)
    
    # 防止重复添加 handler 导致日志打印两次
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # 处理器：输出到控制台
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        
        logger.addHandler(console_handler)
        
        # (可选) 可以在这里添加 FileHandler 将日志写入文件
        
    return logger

# 初始化全局 logger
logger = setup_logger("AI_Translator")
