import os

from sqlalchemy import select, func, insert
from src.database_utils.database_connections import Connection
from src.database_utils.database_schemas import Tables
from src.database_utils.database_second_local_schema import LocalTables
from src.log_utils.logger import Logger
from sqlalchemy.ext.serializer import loads, dumps
import io
import glob

Logger = Logger(logger_name='Requests_log')
logger = Logger.create_logger()

HOST = 'localhost'
PORT = '3307'
DB_USER = 'root'
DB_PASS = 'password'
database = 'sec_db'


class Requests(Tables, LocalTables):
    def __init__(self):
        # Connection.__init__(self)
        Tables.__init__(self)
        LocalTables.__init__(self)
        logger.debug('Schemas was imported')

        self.StatsTable = Tables.StatsTable.__table__
        self.PlayerTable = Tables.PlayersTable.__table__
        self.RoundsTable = Tables.RoundsTable.__table__

        self.LocStatsTable = LocalTables.StatsTable.__table__
        self.LocPlayerTable = LocalTables.PlayersTable.__table__
        self.LocRoundsTable = LocalTables.RoundsTable.__table__
        logger.debug('All tables are inited')

    def create_second_local_mq_tables(self):
        LocalTables.create_tables(self)
        logger.debug('Created tables in local MySQL')

    def insert_second_local_mq_tables(self):
        # data_dict = {'id': 1, 'game_id': 3, 'kills': 55}
        data1_dict = {'id': 1, 'first_name': 'Alesha'}
        # insertion = self.LocStatsTable.insert().values(data_dict)
        insertion_1 = self.LocPlayerTable.insert().values(data1_dict)
        self.sec_local_mq_connection.execute(insertion_1)  #.execute(insertion_1)
        logger.debug('Inserted data in second local MySQL')

    def drop_second_local_mq_tables(self):
        LocalTables.drop_tables(self)
        logger.debug('Dropped tables from second local MySQL')

    def create_local_mq_tables(self):
        Tables.create_tables(self)
        logger.debug('Created tables in local MySQL')

    def insert_local_mq_data(self):
        # TODO Изменить ввод информации под БД CSGO
        data_dict = {'id': 2, 'first_name': 'Losheks', 'last_name': 'Loshara', 'name': 'trt',
                     'hometown': 'Rossia', 'nationality': 'kazah'}
        insertion = self.PlayerTable.insert().values(data_dict)
        self.local_mq_connection.execute(insertion)
        logger.debug('Inserted data in local MySQL')

    def show_local_mq_tables(self):
        request = self.local_mq_connection.execute(self.PlayerTable.select()).fetchall()
        logger.debug('Selected data from local MySQL')
        return request

    def drop_local_mq_tables(self):
        Tables.drop_tables(self)
        logger.debug('Dropped tables from local MySQL')

    def show_mq_tables(self):
        # req = self.mq_connection.execute('SELECT * FROM Stats;').fetchall()  #.execute(select[StatsTable]
        request = self.local_mq_connection.execute(select(func.count()).select_from('Games'))
        logger.debug('Showed tables from MySQL')
        return request

    def get_dump_local_db(self):
        """
        Создаёт дамп базы данных и её данных
        :return:
        """
        Tables.dump_sqlalchemy(self)
        logger.debug('Database was successfully dumped')

    def load_dumped_database(self):
        sec_local_transaction = self.sec_local_mq_connection.begin()
        list_of_requests = glob.glob('../data/dumps/*.sql')
        for req_part in list_of_requests:
            logger.debug(f'{req_part}')
            with io.open(f'{req_part}') as sql_schema:
                dumped_schema = sql_schema.read()
            try:
                self.sec_local_mq_connection.execute(dumped_schema)
                logger.debug('SQL request was created')
            except:
                logger.error('SQL request wasn`t created')
            os.remove(f'{req_part}')

        # Обязательное завершение транзакции
        sec_local_transaction.commit()

    def load_data_into_database(self):
        # TODO Сделать выгрузку данных из Json
        pass


if __name__ == '__main__':
    cl1 = Requests()
    req = cl1.show_mq_tables()
    print(req)
