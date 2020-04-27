# encoding:utf-8
# Motto：good good study, day day up. why you so lazy ？？？


import pytest

from Page.service.ApplicationPage import Application
from Page.service.ServicePage import Service
from Page.service.SetPage import Set
from settings import currentTime
from utils.tools import admin_login, SetUpTestData, param_yaml_object


# @pytest.mark.skip

class TestApplicationManage(object):
    """ 微服务管理-应用管理 """
    AppData = param_yaml_object.read()['AppManage']
    CreateData, DeleteData = [key.values() for key in AppData.values()]

    @pytest.fixture(autouse=True)
    def start(self, driver):
        admin_login(driver)
        self.app_manage = Application(driver)
        self.app_manage.click_Micro_service_manage
        self.app_manage.click_app_manage

    def test_app_search(self):
        """应用名搜索"""
        search_app_name = list(TestApplicationManage.DeleteData)[0]
        self.app_manage.search_app(search_app_name)
        assert self.app_manage.assert_text_in_source([search_app_name, '配置', '删除'])

    @pytest.mark.base_case
    def test_create_app(self):
        """测试创建应用"""
        name, create_expect = TestApplicationManage.CreateData
        self.app_manage.create_app(name, text="UI自动化在{}创建的应用".format(currentTime))
        assert self.app_manage.assert_text_in_source(create_expect), "{}不在Page_source中,断言失败".format(create_expect)

    def test_delete_app(self):
        """测试删除应用"""

        name, delete_expect, search_expect = TestApplicationManage.DeleteData
        self.app_manage.delete_app(name=name)
        delete_result = self.app_manage.assert_text_in_source(delete_expect)
        self.app_manage.search_app(name=name)
        search_result = self.app_manage.assert_text_in_source(search_expect)

        assert search_result == delete_result, "应用{}删除失败".format(name)


# @pytest.mark.skip
class TestServiceManage(object):
    """微服务管理-服务管理"""

    ServiceData = param_yaml_object.read()['ServiceManage']
    InstanceData, CreateData, DeleteData, = [key.values() for key in ServiceData.values()]

    @pytest.fixture(scope='function', autouse=True)
    def start(self, driver):
        admin_login(driver)
        self.service_manage = Service(driver)
        self.service_manage.click_Micro_service_manage
        self.service_manage.click_service_manage

    # @pytest.mark.skip
    @pytest.mark.base_case
    def test_create_service(self):
        """测试创建服务"""
        create_expect, search_expect, service_name = TestServiceManage.CreateData
        self.service_manage.create_service(service_name)
        create_result = self.service_manage.assert_text_in_source(create_expect)
        self.service_manage.search_create_service_success(service_name)
        search_result = self.service_manage.assert_text_in_source(search_expect)

        assert create_result == search_result, "测试创建服务失败"

    # @pytest.mark.skip
    def test_delete_service(self):
        """测试删除服务"""
        delete_expect, search_expect, delete_service_name = TestServiceManage.DeleteData
        self.service_manage.delete_service(name=delete_service_name)
        delete_result = self.service_manage.assert_text_in_source(delete_expect)
        self.service_manage.search_create_service_success(service_name=delete_service_name)
        search_result = self.service_manage.assert_text_in_source(search_expect)

        assert delete_result == search_result, "测试删除服务失败"

    # @pytest.mark.skip
    @pytest.mark.base_case
    def test_create_instance(self):
        """测试创建实例"""
        image_name, instance_name, port = TestServiceManage.InstanceData
        self.service_manage.create_instance(instance_name=instance_name, image_name=image_name, port=port)
        result = self.service_manage.assert_text_in_source(['保存成功!'])

        assert result, "测试创建实例用例失败,保存成功未出现在页面"


#
#
# @pytest.mark.skip
class TestSetManage(object):
    """微服务管理-SET管理"""

    SetData = param_yaml_object.read()['SetManage']
    create, delete = [key.values() for key in SetData.values()]

    @pytest.fixture(scope='function', autouse=True)
    def start(self, driver):
        admin_login(driver)
        self.set_manage = Set(driver)
        self.set_manage.click_Micro_service_manage
        self.set_manage.click_set_manage

    def test_create_set(self):
        """测试创建set"""
        area, group, name = TestSetManage.create
        self.set_manage.create_set(name, area, group)
        create_result = self.set_manage.assert_text_in_source(['创建Set成功'])
        self.set_manage.search_set(name)
        search_result = self.set_manage.assert_text_in_source(list(TestSetManage.create))

        assert create_result == search_result, "测试创建Set失败"

    def test_delete_set(self):
        """测试删除set"""
        delete_set_data = SetUpTestData().create_set
        self.set_manage.delete_set(delete_set_data[0])
        delete_result = self.set_manage.assert_text_in_source(['删除成功'])
        self.set_manage.search_set(delete_set_data[0])
        search_result = self.set_manage.assert_text_in_source(delete_set_data)

        assert delete_result == search_result, "测试删除set失败"
