import os

import time
import configparser


class Config(object):

    def __init__(self, config_file="config.ini") -> None:
        self._path = os.path.join(os.getcwd(), config_file)
        print(self._path)
        time.sleep(4)
        # 判断文件是否存在
        if not os.path.exists(self._path):
            raise FileNotFoundError("没有找到文件：'config.ini'")

        self._config = configparser.ConfigParser()
        self._config.read(self._path, encoding='utf8')

    # 获取值
    def get(self, section, name, strip_blank=True, strip_quote=True) -> str:
        print(self._path)
        s = self._config.get(section, name)

        # 消除空白
        if strip_blank:
            s = s.strip()
            
        # 消除引号
        if strip_quote:
            s = s.strip("'").strip('"')
        return s

    # 判断值是否存在
    def getboolean(self, section, name) -> bool:
        return self._config.getboolean(section, name)

global_config = Config()