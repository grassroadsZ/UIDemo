# encoding:utf-8
# Motto：good good study, day day up. why you so lazy ？？？

import pytest

from Page.system.AuthPage import Auth
from Page.system.UserPage import User
from utils.tools import admin_login, SetUpTestData, TearDownTestData, param_yaml_object


# @pytest.mark.skip
class TestUser(object):
    """用户管理"""

    UserData = param_yaml_object.read()['User']
    create_user, edit_user = UserData['create_user'], UserData['edit_user']

    @pytest.fixture(autouse=True)
    def start(self, driver):
        admin_login(driver)
        self.user_manage = User(driver)
        self.user_manage.click_system_manage
        self.user_manage.click_user_manage

    # @pytest.mark.skip
    @pytest.mark.base_case
    def test_create_user(self):
        """测试新建用户"""

        self.user_manage.create_user(**TestUser.create_user)

        assert self.user_manage.assert_text_in_source("您好，恭喜您创建用户成功！"), "{} 失败".format(self.__doc__)

    # @pytest.mark.skip
    @pytest.mark.base_case
    def test_delete_user_success(self):
        """测试成功删除用户"""
        delete_user = SetUpTestData().create_user
        self.user_manage.delete_user(*delete_user, success=True)
        self.user_manage.search_user(*delete_user)

        assert self.user_manage.get_delete_user_success_info == '暂无数据', "{} 失败".format(self.__doc__)
        # try:
        # assert text == "暂无数据"
        # except AssertionError:
        # TearDownTestData().delete_user(delete_user[0])
        # raise AssertionError("测试删除用户失败")

    # @pytest.mark.skip
    def test_delete_user_fail(self):
        """测试取消删除用户"""
        delete_user_fail = SetUpTestData().create_user
        self.user_manage.delete_user(*delete_user_fail)
        self.user_manage.F5()
        self.user_manage.search_user(*delete_user_fail)
        # 若未删除，则搜索刷新后用户仍然会存在于页面中
        assert self.user_manage.assert_text_in_source(delete_user_fail)

    @pytest.mark.base_case
    def test_edit_user(self):
        """测试编辑用户信息"""
        TearDownTestData().update_user_info
        email, name, phone = list(TestUser.edit_user.values())
        edit_user = SetUpTestData().yaml_to_case_data(random_gen=False)['User']['edit_user'][0]
        self.user_manage.search_user(**edit_user)
        self.user_manage.edit_user_info(**TestUser.edit_user)
        edit_result = self.user_manage.assert_text_in_source(['编辑用户成功'])
        self.user_manage.F5()
        self.user_manage.search_user(**edit_user)

        search_result = self.user_manage.assert_text_in_source([edit_user['user'], email, name, phone])
        # 编辑用户成功出现以及搜索编辑后用户的信息仍然存在视为编辑成功
        assert edit_result == search_result


# @pytest.mark.skip
class TestAuth(object):
    """系统管理-权限管理"""

    @pytest.fixture(scope='function', autouse=True)
    def start_page(self, driver):
        admin_login(driver)
        self.auth_manage = Auth(driver)
        self.auth_manage.click_system_manage
        self.auth_manage.click_auth_manage

    def test_edit_app_auth(self):
        """测试应用权限添加"""
        TearDownTestData().delete_app_auth
        self.auth_manage.edit_app_auth(user='testdata01', insert=True)
        assert self.auth_manage.assert_text_in_source(['应用管理员更新成功']), "{}".format(self.__doc__)
        # 此处权限判断逻辑待完善


#
#
# @pytest.mark.skip
# class TestCloud(object):
#     """集群管理"""
#     url = base_url + 'index.html#/system/cloud'
#
#     @pytest.fixture(scope='function', autouse=True)
#     def start_page(self, driver):
#         self.cloud_manage = Cloud(driver)
#         driver.get(TestCloud.url)
#
#     def test_xx(self):
#         pass


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_system_manage.py::TestUser'])
