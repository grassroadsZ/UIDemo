"""
# -*-conding:utf-8
# @Time:2019-05-21 6:43
# @auther:grassroadsZ
# @file:handle_config.py
"""
import os
from configparser import ConfigParser

from settings import configDir


class HandleConfig(ConfigParser):
    def __init__(self, filename=os.path.join(configDir, "case_config.conf")):
        # 继承父类，同时重写父类self.filename属性
        super().__init__()
        self.filename = filename

    def __call__(self, section, option=None, is_eval=False, is_bool=False):
        self.read(self.filename, encoding="utf-8")
        if option is None:
            return dict(self[section])

        if isinstance(is_bool, bool):
            if is_bool:
                return self.getboolean(section, option)
            # else:
            #     return self.get( section , option )
        else:
            raise ValueError("is_bool的值必须是布尔类型")

        data = self.get(section, option)
        if data.isdigit():
            return int(data)
        try:
            return float(data)
        except Exception:
            pass

        if isinstance(is_eval, bool):
            if is_eval is True:
                return eval(self.get(section, option))
            # else:
            #     return self.get( section , option )
        else:
            raise ValueError("is_bool的值必须是布尔类型")

        return data


do_config = HandleConfig()


if __name__ == '__main__':
    # do_config.config_write(data= 1, filename = "user.conf")
    print(do_config("log"))
