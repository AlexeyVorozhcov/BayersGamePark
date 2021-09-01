
import my_logging
import my_logging_test_2

logger = my_logging.get_logger(__name__)

def main():
    logger.info("Программа стартует")
    my_logging_test_2.process(msg="сообщение")
    logger.warning("Это должно появиться как в консоли, так и в файле журнала")
    logger.info("Программа завершила работу")

if __name__ == "__main__":
    main()