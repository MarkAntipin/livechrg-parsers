import logging


def create_logger(level=logging.DEBUG) -> logging.Logger:
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    logger.addHandler(console_handler)

    return logger
