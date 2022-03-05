import configparser
import os
from src.log_utils.logger import Logger

Logger = Logger(logger_name='Config_utils_log')
logger = Logger.create_logger()


class ConfigClass:
    def __init__(self):
        self.path_to_config = '../data/configs/program_configs.ini'
        self.sections = ['Checkpoints', 'Settings']
        self.create_config()

    def create_config(self):
        self.config = configparser.ConfigParser()

        # Чекпоинты
        self.config.add_section(f"{self.sections[0]}")
        self.config.set(f"{self.sections[0]}", "is_dump", "0")

        # Настройки
        self.config.add_section(f"{self.sections[1]}")
        self.config.set(f"{self.sections[1]}", "-", "False")

        if not os.path.exists(self.path_to_config):
            with open(self.path_to_config, "w") as config_file:
                self.config.write(config_file)
                logger.debug('Config is created')
        else:
            self.readed_config = self.get_config()
            self.update_config('Checkpoints', 'is_dump', '0')

    def get_config(self):
        self.config.read(self.path_to_config)
        return self.config

    def update_config(self, section, param, value):
        self.readed_config = self.get_config()
        self.readed_config.set(section, param, value)
        with open(self.path_to_config, "w") as config_file:
            self.readed_config.write(config_file)
            logger.debug('Config was updated')


# def edit_config(command):
#     with open(path, "w") as config_file:
#         config.write(config_file)
