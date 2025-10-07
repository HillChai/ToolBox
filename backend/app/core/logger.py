import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from app.core.config import settings

def setup_logger():
    logger = logging.getLogger("app")
    logger.setLevel(settings.LOG_LEVEL)

    # 避免重复添加 handler（热重载/多次调用）
    if logger.handlers:
        return logger

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    if settings.LOG_TO_FILE:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True, parents=True)
        fh = RotatingFileHandler(log_dir / "app.log", maxBytes=2_000_000, backupCount=3)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    else:
        sh = logging.StreamHandler()  # stdout
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    # 可选：把 uvicorn 的日志也统一到同一格式
    logging.getLogger("uvicorn.access").handlers = logger.handlers
    logging.getLogger("uvicorn.error").handlers = logger.handlers

    return logger

logger = setup_logger()
