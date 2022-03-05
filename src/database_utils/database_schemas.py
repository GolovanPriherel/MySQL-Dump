from sqlalchemy import MetaData, Table, Integer, Column, Text, BIGINT, Float, DateTime, ForeignKey, ForeignKeyConstraint,\
    Index, PrimaryKeyConstraint, create_engine
from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy.orm import mapper, scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from src.database_utils.database_connections import Connection
from sqlalchemy_mixins import AllFeaturesMixin
from src.log_utils.logger import Logger
from src.file_utils.config_utils import ConfigClass
import time, json, io

# conn_class = Connection()

Logger = Logger(logger_name='Schema_log')
logger = Logger.create_logger()

local_mq_engine = create_engine("mysql+pymysql://user:password@mysql_container/db")
metadata = MetaData(bind=local_mq_engine)
session = scoped_session(sessionmaker())
Base = declarative_base(metadata=metadata)


class BaseModel(Base, AllFeaturesMixin):
    __abstract__ = True
    pass


class Tables(ConfigClass):
    def __init__(self):
        self.local_mq_engine = local_mq_engine
        self.buf = io.BytesIO()
        ConfigClass.__init__(self)
        while True:
            try:
                self.local_mq_connection = self.local_mq_engine.connect()
                if self.local_mq_connection:
                    break
            except:
                logger.debug('Trying connect to second local MqSQL')
                time.sleep(5)

    class PlayersTable(BaseModel):
        __tablename__ = 'Players'
        id = Column(BIGINT, nullable=False, default=0, primary_key=True, autoincrement=True)
        birthdate = Column(DateTime)
        first_name = Column(Text)
        last_name = Column(Text)
        name = Column(Text)
        hometown = Column(Text)
        nationality = Column(Text)

    class RoundsTable(BaseModel):
        __tablename__ = 'Rounds'
        id = Column(BIGINT, primary_key=True, nullable=False, autoincrement=True)
        game_id = Column(BIGINT, nullable=False)
        ct_id = Column(BIGINT, nullable=False)
        t_id = Column(BIGINT, nullable=False)
        winner_id = Column(BIGINT, nullable=False)
        round = Column(BIGINT)
        winner_side = Column(Text)
        outcome = Column(Text)

    class StatsTable(BaseModel):
        __tablename__ = 'Stats'
        id = Column(BIGINT, primary_key=True, nullable=False, autoincrement=True)
        game_id = Column(BIGINT, nullable=False, default=0)
        player_id = Column(BIGINT, ForeignKey('Players.id'), nullable=False, default=0)
        assists = Column(Integer)
        deaths = Column(Integer)
        flash_assists = Column(Integer)
        headshots = Column(Integer)
        kills = Column(Integer)
        adr = Column(Float)
        first_kill_diff = Column(Float)
        k_d_diff = Column(Float)
        kast = Column(Float)
        rating = Column(Float)

    def create_tables(self):
        metadata.create_all(local_mq_engine)
        metadata.reflect(bind=local_mq_engine)  # http://docs.sqlalchemy.org/en/rel_0_9/core/reflection.html

    def drop_tables(self):
        metadata.drop_all(local_mq_engine)

    def dump_sqlalchemy(self):
        """ Returns the entire content of a database as lists of dicts"""
        result = {}
        # Перенос данных
        for table in metadata.sorted_tables:
            result[table.name] = [dict(row) for row in local_mq_engine.execute(table.select())]

        # Перенос структуры базы данных
        def dump(sql, *multiparams, **params):
            f = sql.compile(dialect=local_mq_engine.dialect)
            self.buf.write(str(f).encode('utf-8'))
            self.buf.write(b';-+-+-')

        # Чтение конфига
        readed_config = self.get_config()

        if readed_config['Checkpoints']['is_dump'] == '0':
            local_mq_dump_engine = create_engine("mysql+pymysql://user:password@mysql_container/db", strategy='mock',
                                                 executor=dump)
            metadata.create_all(bind=local_mq_dump_engine, checkfirst=True)

        schema_text = self.buf.getvalue().decode(encoding='utf-8')
        schema_text = schema_text.split('-+-+-')[:-1]

        # Разбиение SQL-запроса на части
        for i, sql_req in enumerate(schema_text):
            with open(f'../data/dumps/schema{i}.sql', 'wb+') as sql_file:
                sql_file.write(sql_req.encode(encoding='utf-8'))
        logger.debug('Schema of database was dumped')

        # Дамп данных из БД
        with open('../data/dumps/dumped_data_of_first_schema.json', 'w') as json_file:
            json.dump(result, json_file)
        self.update_config('Checkpoints', 'is_dump', '1')
        logger.debug('Data of database was dumped')
