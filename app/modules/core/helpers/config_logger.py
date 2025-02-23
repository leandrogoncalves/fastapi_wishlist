import logging
from modules.core.helpers.loggin_json_formatter import LoggingJsonFormatter


def get_logger():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(LoggingJsonFormatter())
    logger = logging.getLogger(__name__)
    logger.handlers.clear()
    logger.addHandler(stream_handler)
    logging.getLogger().setLevel(logging.DEBUG)
    return logger
