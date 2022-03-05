from sqlalchemy import MetaData, Integer, Column, Text, BIGINT, Float, DateTime, ForeignKey, ForeignKeyConstraint,\
    Index, PrimaryKeyConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
# from src.database_utils.database_connections import Connection
from src.log_utils.logger import Logger
import time
from sqlalchemy_mixins import AllFeaturesMixin

# conn_class = Connection()

Logger = Logger(logger_name='Second_schema_log')
logger = Logger.create_logger()

sec_local_mq_engine = create_engine("mysql+pymysql://user:password@second_mysql_container/sec_db")
metadata = MetaData(bind=sec_local_mq_engine)
Base = declarative_base(metadata=metadata)


class BaseModel(Base, AllFeaturesMixin):
    __abstract__ = True
    pass


class LocalTables:
    def __init__(self):
        self.sec_local_mq_engine = sec_local_mq_engine
        while True:
            try:
                self.sec_local_mq_connection = self.sec_local_mq_engine.connect()
                if self.sec_local_mq_connection:
                    break
            except:
                logger.debug('Trying connect to second local MqSQL')
                time.sleep(5)

    class PlayersTable(BaseModel):
        __tablename__ = 'Players'
        id = Column(BIGINT, nullable=False, default=0, primary_key=True)
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
        metadata.create_all(sec_local_mq_engine)

    def drop_tables(self):
        metadata.drop_all(sec_local_mq_engine)
