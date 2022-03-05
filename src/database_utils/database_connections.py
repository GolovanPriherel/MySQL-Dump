import pymysql.cursors
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.log_utils.logger import Logger
import pymysql

Logger = Logger(logger_name='Connections_log')
logger = Logger.create_logger()


class Connection:
    def __init__(self):
        # Создание движка и сессии для подключения к MySQL
        # try:
        #     self.mq_engine = create_engine("mysql+pymysql://analitic:tic456an@91.241.59.60/csgo_db")
        #     logger.debug('Created MySQL engine')
        #     self.mq_session = sessionmaker(bind=self.mq_engine)
        #     logger.debug('Created MySQL session')
        #     self.mq_connection = self.mq_engine.connect()
        #     logger.debug('Created MySQL connection')
        # except:
        #     logger.error('Creation of MySQL engine/session/connection is failed')
        #     # raise

        # Создание движка для локальной MySQL
        self.local_mq_engine = create_engine("mysql+pymysql://user:password@mysql_container/db")  # Здесь указывать вместо localhost'a имя контейнера, где расположена БД
        logger.debug('Engine to local MqSQL was created')
        self.local_mq_connection = self.local_mq_engine.connect()
        logger.debug('Connection to local MqSQL was created')

        # Создание движка для второй локальной MySQL для тестирования миграции
        # self.local2_mq_engine = create_engine("mysql+pymysql://user:password@second_mysql_container/sec_db")  # Здесь указывать вместо localhost'a имя контейнера, где расположена БД
        # logger.debug('Engine of second local MqSQL was created')
        self.local2_mq_connection = self.local2_mq_engine.connect()
        logger.debug('Connection to second local MqSQL was created')


if __name__ == '__main__':
    pass
    # cl1 = Connection()
