## src/app/core/logger.py

import logging.config
# 引入 uvicorn 的日志格式化器（自带颜色处理）
from uvicorn.logging import DefaultFormatter

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            # 使用 Uvicorn 的 DefaultFormatter
            "()": "uvicorn.logging.DefaultFormatter",
            # %(levelprefix)s 是 Uvicorn 特有的，它会自动根据级别显示颜色（如绿色的 INFO:，红色的 ERROR:）
            "fmt": "%(levelprefix)s %(asctime)s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": True,
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        # 1. 配置根日志 (Root Logger)
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        # 2. 配置你的应用日志
        "app": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,  # 【关键修复】设置为 False，防止日志向上传递导致重复打印
        },
        # 3. 强制覆盖 uvicorn 的日志配置，使其与你的格式保持一致
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

def configure_logging():
    """应用日志配置"""
    logging.config.dictConfig(LOGGING_CONFIG)


#import logging.config
#
## 定义日志配置字典 (DictConfig)
## 这是企业级项目最常用的配置方式
#LOGGING_CONFIG = {
#    "version": 1,
#    "disable_existing_loggers": False,  # 非常重要：保持 False，否则会把 Uvicorn 的日志关掉
#    "formatters": {
#        "standard": {
#            # 格式：时间 - 级别 - 模块名 - 消息
#            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
#            "datefmt": "%Y-%m-%d %H:%M:%S",
#        },
#    },
#    "handlers": {
#        "console": {
#            "level": "INFO",
#            "class": "logging.StreamHandler",
#            "formatter": "standard",
#        },
#        # 如果以后想写文件，可以在这里加 "file_handler"
#    },
#    "loggers": {
#        # 配置根日志 (Root Logger)
#        "": {
#            "handlers": ["console"],
#            "level": "INFO",
#            "propagate": True,
#        },
#        # 专门针对我们自己的 app 应用
#        "app": {
#            "handlers": ["console"],
#            "level": "INFO",
#            "propagate": False,
#        },
#    },
#}
#
#def configure_logging():
#    """应用日志配置"""
#    logging.config.dictConfig(LOGGING_CONFIG)
#
#configure_logging()
