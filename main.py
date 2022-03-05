import uvicorn, os
from fastapi import FastAPI, Form
from src.database_utils.database_requests import Requests
from src.log_utils.logger import Logger
from src.file_utils.config_utils import ConfigClass

Logger = Logger(logger_name='Main_log')
logger = Logger.create_logger()

req_class = Requests()
# logger.debug('Connections complete')
app = FastAPI()


@app.get("/")
async def root():
    return 'Сервис готов к работе.'


@app.get("/create_table/")
async def serv_create_local_mq_tables():
    try:
        req_class.create_local_mq_tables()
    except:
        raise
    return 'Готово'


@app.get("/show_data/")
async def serv_show_local_mq_tables():
    try:
        request = req_class.show_local_mq_tables()
    except:
        raise
    return request


# @app.post("/put_data/")
# async def serv_put_data_in_ch_tables():
#     try:
#         req_class.insert_local_mq_data()
#     except:
#         raise
#     return 'Готово'


@app.get("/insert_data/")
async def serv_insert_local_mq_tables():
    try:
        req_class.insert_local_mq_data()
    except:
        raise
    return 'Готово'


@app.get("/drop_table/")
async def serv_drop_local_mq_tables():
    try:
        req_class.drop_local_mq_tables()
    except:
        raise
    return 'Готово'


@app.get("/create_second_table/")
async def serv_create_second_local_mq_tables():
    try:
        req_class.get_dump_local_db()
        req_class.load_dumped_database()
    except:
        raise
    return 'Готово'


@app.get("/insert_data_second_table/")
async def serv_drop_second_local_mq_tables():
    try:
        req_class.insert_second_local_mq_tables()

    except:
        raise
    return 'Готово'


@app.get("/drop_second_table/")
async def serv_drop_second_local_mq_tables():
    try:
        req_class.drop_second_local_mq_tables()
    except:
        raise
    return 'Готово'


# @app.get("/dump_data/")
# async def serv_dump_data_from_db():
#     try:
#         req_class.get_dump_local_db()
#     except:
#         raise
#     return 'Готово'


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
    logger.debug('Service is running')
