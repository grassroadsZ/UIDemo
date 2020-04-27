# -*- encoding:utf-8 -*-
"""
@Author: grassroadsZ
@data: 2020/4/15 11:32
@file: handle_thread
"""

import threading

from utils.tools import api_login, api_option, TearDownTestData


class MyThread(threading.Thread):
    """
    线程池清理
    """

    def __init__(self, func, args=()):
        """
        :param func: 任务名
        :param args: 任务的参数
        """
        super().__init__()
        self.task = func
        self.args = args

    def run(self):
        self.result = self.task(*self.args)

    @property
    def get_result(self):
        try:
            return self.result
        except AttributeError:
            return None

    @staticmethod
    def api_get_data(name: str, method='get', data={}):
        """
        获取需要删除的测试数据
        :param name:str: 接口名称：name=get_application_list --> /pages/server/api/get_application_list
        :param method: method='get'
        :return:
        """
        # data = None
        try:
            data = api_login(method=method, uri='pages/server/api/{}'.format(name), data=data)
        except Exception as e:
            raise e
        return data.json()

    @staticmethod
    def get_delete_data(args_dict: dict) -> dict:
        """
        获取所有需要删除的接口数据集数据，每个接口一个线程
        :param args_dict: {"get_application_list": "get", "get_server_list": "post", "get_set_list": "get"}
        :return:{get_server:JsonResponse,get_user:JsonResponse}
        """
        t_pool = []
        result = {}
        for task in args_dict:
            t = MyThread(func=MyThread.api_get_data, args=(task, args_dict.get(task)))
            t.setName(task)
            t.start()
            t_pool.append(t)

        for t in t_pool:
            t.join()

            result.setdefault(t.getName(), t.get_result.get('data'))
        return result

    def before_start_delete_data(self, args_dict: dict):
        data_dict = self.get_delete_data(args_dict)
        instance_list = api_option('get_deploy_list', data={"application": "TarsUIAuto", "server_name": "ApiToTarsUI"})
        instance_name_list = [key['deployment_name'] for key in instance_list.json()['data']]

        if data_dict.get("get_application_list"):
            app_list = [key['application'] for key in data_dict.get("get_application_list") if
                        'TarsUIApp' in key['application']]

            for app in app_list:
                TearDownTestData().delete_app(app)

        if data_dict.get('get_server_list'):
            server_list = [key['server_name'] for key in data_dict.get('get_server_list') if
                           'TarsUIAuto' in key['application'] and key['deploy_count'] == 0 and key[
                               'server_name'] != 'ApiToTarsUI']

            for server in server_list:
                TearDownTestData().delete_service(server)

        if data_dict.get('get_set_list'):
            set_list = [key for key in data_dict.get('get_set_list') if key['set_name'] != 'set1']

            for d in set_list:
                d.pop('create_time')
                d.pop('description')
                d.pop('posttime')
                d.pop('id')
            for s in set_list:
                TearDownTestData().delete_set(s)

        if data_dict.get('list_user'):
            user_list = [user['user'] for user in data_dict.get('list_user') if 'Tars' in user['user']]

            for user in user_list:
                TearDownTestData().delete_user(user)

        if instance_name_list:
            for instance in instance_name_list:
                TearDownTestData().delete_instance(instance)


if __name__ == '__main__':
    name = {"get_application_list": "get", "get_server_list": "post", "get_set_list": "get", "list_user": 'post'}

    print(MyThread(MyThread.get_delete_data(name)).before_start_delete_data(name))

# t_pool = []
# result = {}
# for task in name:
#     t = MyThread(func=MyThread.api_get_data, args=(task, name[task]))
#     t.setName(task)
#     t.start()
#     t_pool.append(t)
#
# for t in t_pool:
#     t.join()
#     # print(t.get_result())
#     result[t.getName()] = t.get_result()


# thread_pool = []
# 创建两个线程任务(异步创建)
# for i in name:
#     t = threading.Thread(target=get_test_data, args=(i, name[i]))
#     thread_pool.append(t)
# # t2 = threading.Thread(target=get_test_data, args=())
# # 启动线程
# for i in thread_pool:
#     i.start()
# for i in thread_pool:
#     i.join()
# t2.start()
# 设置主线程等待子线程执行完后再执行
# t1.join()
# t2.join()