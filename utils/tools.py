import hashlib
import os
import random
from datetime import datetime

import faker

from Page.LoginPage import Login
from settings import private_user_info, base_url, currentTime, dataDir
from utils.handle_log import MyLog
from utils.handle_requests import MyRequests
from utils.handle_yaml import HandleYaml

log = MyLog().out()
param_yaml_object = HandleYaml(os.path.join(dataDir, 'param_case_data.yaml'))
constant_yaml_object = HandleYaml(os.path.join(dataDir, 'constant_case_data.yaml'))

faker_en = faker.Faker()
faker_cn = faker.Faker('zh_CN')


def admin_login(driver):
    """UI层面的admin登录"""
    login_page = Login(driver)
    login_page.login(username=private_user_info['username'], password=private_user_info['password'])


def api_login(uri, data, method='post'):
    """
    admin接口登录使用
    :param uri: base_url后面部分
    :param data: json数据
    :return:
    """
    admin_api_login = MyRequests()
    admin_api_login(method='post', url=base_url + 'pages/server/api/login', is_json=True,
                    data={'user': private_user_info['username'],
                          "passwd": hashlib.md5(private_user_info['password'].encode('utf-8')).hexdigest()})

    return admin_api_login(method=method, url=base_url + uri, is_json=True, data=data)


def api_option(url: str, data: dict):
    """
    接口删除服务、应用、set等测试生成数据的基础函数
    :param url: del_delete_app --> pages/server/api/del_delete_app
    :param data: {}
    """
    try:
        resp = api_login(uri='pages/server/api/{}'.format(url), data=data)
    except Exception:
        raise Exception("通过接口 {} 失败".format(url))
    if resp.status_code == 200 and resp.json().get('ret_code') == 0:
        log.info("{} 成功".format(url))
        return resp


class SetUpTestData(object):
    """
    制造测试数据
    """

    @staticmethod
    def generate_random_param_yaml_file():
        """生成参数化case需要用到的数据到yaml文件
        eg:yaml_object.write(data="PageClass": {"function": [{"user": user, "name": user, "phone": faker_cn.phone_number(),
                                                         "email": faker_cn.email(),
                                                         },
                                                         {"user": user, "name": user, "phone": faker_cn.phone_number(),
                                                          "email": faker_cn.email()}
                                                         ]
                                         }
        :return:PageClass:
                    function:
                      - arg_1: nahe@96.cn
                        name: TarsMichaelBrown
                        phone: '13962846767'
                        user: TarsMichaelBrown
                      - arg_2: xiuying54@yahoo.com
                        name: TarsMichaelBrown
                        phone: '18611688498'
                        user: TarsMichaelBrown
        """
        user = "Tars" + faker_en.name().replace(' ', '').replace('.', '')
        now_time = datetime.now().strftime("%m%d%H%M%S")
        param_yaml_object.write(
            data={"User": {"create_user": {"user": user, "name": user, "phone": faker_cn.phone_number(),
                                           "email": faker_cn.email(),
                                           "description": '这是UI自动化运行前生成的数据'},
                           "edit_user": {"name": user, "phone": faker_cn.phone_number(),
                                         "email": faker_cn.email()},

                           },
                  "AppManage": {
                      "create_app": {"app_name": 'TarsUIApp{}'.format(now_time), "create_expect": '创建应用成功'},
                      "delete_app": {"app_name": SetUpTestData().create_app, "delete_expect": "删除成功",
                                     "search_expect": '暂无数据'}},
                  "ServiceManage": {
                      "create_service": {"service_name": 'TarsUiService{}'.format(now_time), "create_expect": '创建服务成功',
                                         "search_expect": ['创建实例', '查看实例', '删除']},
                      "delete_service": {"service_name": SetUpTestData().create_service, "delete_expect": '删除成功',
                                         "search_expect": '暂无数据'},
                      "create_instance": {"instance_name": 'Instance{}'.format(now_time),
                                          "image_name": 'node1:5000/test2/tmecweb:v1.0.0',
                                          "port": random.randint(9999, 60000)}},
                  "SetManage": {
                      "create_set": {"set_name": 'SetName{}'.format(faker_cn.user_name()),
                                     "area": 'SetArea{}'.format(faker_en.user_name().replace(' ', "")),
                                     "group": random.randint(1, 255)},
                      "delete_set": {"app_name": SetUpTestData().create_app, "delete_expect": "删除成功",
                                     "search_expect": '暂无数据'}},

                  })

    def yaml_to_case_data(self, random_gen=True):
        """
        读取yaml数据生成测试数据
        :param random_gen:是否生成随机的数据
        :return:
        """
        if random_gen:
            self.generate_random_param_yaml_file()
            content = param_yaml_object.read()
        else:
            content = constant_yaml_object.read()
        return content

    @staticmethod
    def cp_report(report_dir):
        """
        备份报告文件
        :param report_dir: 报告路径
        :return:
        """
        if os.path.exists(os.path.join(report_dir, 'ST_result_bk.html')): os.remove(
            os.path.join(report_dir, 'ST_result_bk.html'))
        for file in os.listdir(report_dir):
            if file == 'ST_result.html': os.renames(os.path.join(report_dir, 'ST_result.html'),
                                                    os.path.join(report_dir, 'ST_result_bk.html'))

    @property
    def create_app(self):
        """
        使用接口创建微服务管理页面-应用的搜索删除的前置数据
        :return: 调用pages/server/api/add_app 接口进行app的创建
        """
        data = {"name": "TarsUIApp" + faker_en.name().replace(' ', '').replace('.', ''),
                "description": "UI自动化在{}为删除应用创建的应用".format(currentTime)}
        api_option('add_app', data)
        return data['name']

    @property
    def create_service(self):
        """
        使用接口创建服务管理页面-删除服务测试用例需要的服务
        :return: 调用pages/server/api/create_server 接口进行service的创建
        """
        data = {"application": "TarsUIAuto", "server_name": "Tars{}".format(faker_en.user_name())}

        api_option('create_server', data)
        return data['server_name']

    @property
    def create_instance_service(self):
        """
        使用接口创建服务管理页面-删除服务测试用例需要的服务
        :return: 调用pages/server/api/create_server 接口进行创建实例所需要service的创建
        """
        data = {"application": "TarsUIAuto", "server_name": "ApiToTarsUI"}

        api_option('create_server', data)

        return data['server_name']

    @property
    def create_user(self):
        """
        使用接口创建系统管理-用户管理-新建用户case产生的测试数据
        :return: 调用pages/server/api/add_user 接口进行用户的的创建
        """
        data = {"user": "Tars{}".format(faker_en.name().replace(' ', '')), "name": "Tars{}".format(faker_cn.name()),
                "phone": faker_cn.phone_number(),
                "email": faker_cn.email(), "passwd": hashlib.md5("Abc123456".encode('utf-8')).hexdigest(),
                'comments': "UI自动化通过接口生成的用户"}

        api_option('add_user', data)

        data.pop('passwd')
        data.pop('comments')

        return list(data.values())

    @property
    def create_set(self):
        """
        使用接口创建微服务管理-SET管理case所需要的set的测试数据
        :return: 调用pages/server/api/create_set 接口进行set的的创建
        """
        data = {"set_name": 'SetName{}'.format(faker_cn.user_name()),
                "set_area": 'SetArea{}'.format(faker_en.user_name().replace(' ', "")),
                "set_group": random.randint(1, 255)}
        api_option('create_set', data)

        return list(data.values())


class TearDownTestData(object):
    """
    使用接口进行测试数据后置清理所需要的接口
    """

    def delete_app(self, name):
        """
        使用接口删除微服务管理页面的应用
        :param name: app应用名
        :return 调用pages/server/api/delete_app 接口进行app的删除
        """
        data = {"name": "{}".format(name)}
        return api_option('delete_app', data)

    def delete_service(self, name):
        """
        使用接口删除服务管理页面-创建服务产生的测试数据
        :param name: service服务名
        :return 调用pages/server/api/del_server 接口进行service的删除
        """
        data = {"application": "TarsUIAuto", "server_name": "{}".format(name)}
        return api_option('del_server', data)

    def delete_set(self, delete_data):
        """
        使用接口删除set管理页面产生的测试数据
        :param delete_data:删除的set的json数据 {"set_name":"SetNamenmeng","set_group":16,"set_area":"SetAreahalldenise"}
        :return 调用pages/server/api/delete_set 接口进行set的删除
        """
        return api_option('delete_set', delete_data)

    def delete_instance(self, instance_name):
        """
        使用接口删除服务管理页面-创建实例产生的测试数据
        :param instance_name:
        :return 调用pages/server/api/del_deploy 接口进行实例的删除
        """
        data = {"application": "TarsUIAuto", "server_name": 'ApiToTarsUI',
                "deployment_name": "{}".format(instance_name)}
        return api_option('del_deploy', data)

    def delete_user(self, user):
        """
        使用接口删除系统管理-用户管理-新建用户case产生的测试数据
        :param user:
        :return 调用pages/server/api/delete_user 接口进行用户的删除
        """
        data = {"user": "{}".format(user)}
        return api_option('delete_user', data)

    @property
    def update_user_info(self):
        """
        将已有的测试账号testdata01数据恢复
        :return: 调用pages/server/api/update_user 接口进行用户testdata01的权限的的还原
        """
        data = {"user": "testdata01", "name": "测试数据", "phone": "18000000002", "email": "testdata01@qq.com",
                "comments": "UI自动化测试账号，勿删除."}
        return api_option('update_user', data)

    @property
    def delete_app_auth(self):
        """
        使用接口将用户testdata01的权限还原为无TarsUIAuto权限状态
        """
        data = {"admins": [{"role": "app_mgr", "users": [], "current_update_users": ["testdata01"]}],
                "application": "TarsUIAuto"}
        api_option('update_application_admins', data)


if __name__ == '__main__':
    print(param_yaml_object.read())
