import logging

from core.config import settings


def get_logger(name:str = "app"):
    logger = logging.getLogger(name=name)
    if not logger.handlers:
        if settings.DEBUG:
            logger.setLevel(level=logging.DEBUG)
        else:
            logger.setLevel(level=logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt='[%(asctime)s] %(levelname)s - %(name)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger