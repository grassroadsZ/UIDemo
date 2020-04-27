# encoding:utf-8
# Motto：good good study, day day up. why you so lazy ？？？
"""
对yaml文件的读取与写入，解决多线程数据不一致的问题
"""
import os

import yaml

from settings import dataDir


class HandleYaml(object):
    """
    yaml文件处理
    """

    def __init__(self, file_path: str):
        if '.yaml' not in file_path:
            raise TypeError("文件{}必须是yaml格式的文件".format(file_path))
        self.file = file_path

    def read(self):
        with open(self.file, mode='r', encoding='utf-8') as f:
            data = yaml.load(f.read(), Loader=yaml.FullLoader)
            f.close()
            return data

    def write(self, data):
        """
        先对需要写入的data进行判断,当需要写入的data的key存在，则修改value,不存在则写入
        :param data:
        :return:
        """
        if self.read() is None:
            with open(self.file, mode='w', encoding='utf-8') as f:
                yaml.dump(data=data, stream=f, allow_unicode=True)
                return

        tmp_data = self.read()

        exist_file_data = deep_update_dict(dict(tmp_data), data)

        with open(self.file, mode='w', encoding='utf-8') as f:
            yaml.dump(data=exist_file_data, stream=f, allow_unicode=True)


def deep_update_dict(origin_dict, override_dict):
    """ update origin dict with override dict recursively
    e.g. origin_dict = {'a': 1, 'b': {'c': 2, 'd': 4}}
         override_dict = {'b': {'c': 3}}
    return: {'a': 1, 'b': {'c': 3, 'd': 4}}
    """
    if not override_dict:
        return origin_dict

    for key, val in override_dict.items():
        if isinstance(val, dict):
            tmp = deep_update_dict(origin_dict.get(key, {}), val)
            origin_dict[key] = tmp
        elif val is None:
            # fix #64: when headers in test is None, it should inherit from config
            continue
        else:
            origin_dict[key] = override_dict[key]

    return origin_dict


if __name__ == '__main__':
    y = HandleYaml(os.path.join(dataDir, 'case_data.yaml'))
    # print(y.read())
    y.write(data={"AppManageData": {"create_app": {"app_name": 'UIApp1', "expect": ['创建应用成功']},
                                    "delete_app_expect": {'expect_1': ['暂数据'], 'expect_2': ['删除成功']},
                                    "delete_app_expect_1": {'expect_1': ['暂数据'], 'expect_2': ['删除成功']}}
                  })

    y.write(data={"AppManageData": {"create_app": {"app_name": 'UIApp1000', "expect": ['创建应用不成功']},
                                    "在app": {'expect_1': ['暂数据'], 'expect_2': ['删除成功']}}
                  })
