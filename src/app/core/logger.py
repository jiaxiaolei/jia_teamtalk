import logging
import logging.config
import sys
import copy

class TornadoLogFormatter(logging.Formatter):
    """
    仿 Tornado 风格的日志格式化器
    格式: [I 251216 13:28:00 module:line] message
    """
    # ANSI 颜色代码
    COLOR_NORMAL = "\033[0m"
    COLOR_RED = "\033[1;31m"
    COLOR_GREEN = "\033[1;32m"
    COLOR_YELLOW = "\033[1;33m"
    COLOR_BLUE = "\033[1;34m"
    COLOR_MAGENTA = "\033[1;35m"
    COLOR_CYAN = "\033[1;36m"

    LEVEL_COLORS = {
        logging.DEBUG: COLOR_BLUE,
        logging.INFO: COLOR_GREEN,
        logging.WARNING: COLOR_YELLOW,
        logging.ERROR: COLOR_RED,
        logging.CRITICAL: COLOR_MAGENTA,
    }

    def format(self, record):
        record = copy.copy(record)
        color = self.LEVEL_COLORS.get(record.levelno, self.COLOR_NORMAL)

        # Tornado 风格时间: YYMMDD HH:MM:SS
        record.asctime = self.formatTime(record, datefmt="%y%m%d %H:%M:%S")

        # 级别首字母
        level_letter = record.levelname[0]

        # 格式: [I 230909 10:00:00 main:25]
        prefix = f"[{level_letter} {record.asctime} {record.module}:{record.lineno}]"

        formatted_message = f"{color}{prefix}{self.COLOR_NORMAL} {record.getMessage()}"

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            formatted_message += "\n" + record.exc_text

        return formatted_message

# 定义配置字典
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "tornado": {
            # 直接使用上面的类
            "()": TornadoLogFormatter,
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "tornado",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        # 根日志：接管所有未配置的日志
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        # 应用日志
        "app": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        # 强制接管 Uvicorn 内部日志
        "uvicorn": { "handlers": ["console"], "level": "INFO", "propagate": False },
        "uvicorn.error": { "handlers": ["console"], "level": "INFO", "propagate": False },
        "uvicorn.access": { "handlers": ["console"], "level": "INFO", "propagate": False },
    },
}

def configure_logging():
    """手动应用配置 (用于非 uvicorn.run 启动的场景)"""
    logging.config.dictConfig(LOGGING_CONFIG)
