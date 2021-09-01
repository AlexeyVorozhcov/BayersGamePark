import my_logging

logger = my_logging.get_logger(__name__)

def process(msg):
    logger.info("Перед процессом")
    print(msg)
    logger.info("После процесса")