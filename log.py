import logging
from logging.handlers import RotatingFileHandler


def setup_logger(logger):
    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format = logFormatStr, filename = "logs/global.log", level=logging.DEBUG)
    formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')
    fileHandler = logging.FileHandler("logs/summary.log")
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    my_handler = RotatingFileHandler("logs/global.log", mode='w', maxBytes=50*1024*1024,
                                 backupCount=2, delay=0)
    my_handler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
    logger.addHandler(my_handler)

    logger.info("Logging is set up.")
