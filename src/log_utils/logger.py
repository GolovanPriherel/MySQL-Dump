import logging
import sys, time
from logging import StreamHandler, Formatter, LogRecord


class Logger:
    def __init__(self, path='/Logs/', logger_name='default_logger', filename='CSGO_Log'):
        self.path = path
        self.logger_name = logger_name
        self.filename = filename

    def create_logger(self):
        logfile = str(self.path + (time.strftime(f"""{self.filename}_%d.%m.%Y_%H:%M:%S""", (time.localtime()))) + '.log')
        logging.basicConfig(level=logging.DEBUG,
                            filename=logfile,
                            format="%(asctime)s — %(name)s — %(levelname)s — %(message)s")

        logger = logging.getLogger(self.logger_name)
        logger.setLevel(logging.DEBUG)

        handler = StreamHandler(stream=sys.stdout)

        logger.addHandler(handler)
        return logger


if __name__ == '__main__':
    logclass = Logger(logger_name='4mo')
    logger = logclass.create_logger()
    logger.debug('Mat')

