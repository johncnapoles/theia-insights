import logging

from constants.data_constants import PATH


def create_logger(logger_name, console_logging=True):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s.%(msecs)03d][%(levelname)s]%(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    # Configure File Handler for log file saving
    file_handler = logging.FileHandler(
        filename=f"{PATH.LOG_DIRECTORY.value}/{logger_name}.log"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Configure Stream Handler for console outputs
    if console_logging:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
