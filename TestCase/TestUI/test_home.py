# encoding:utf-8
# Motto：good good study, day day up. why you so lazy ？？？

import pytest

from Page.LoginPage import Login
from Page.home.HomePage import Home
from utils.tools import admin_login, SetUpTestData, constant_yaml_object


class TestHomePage(object):
    """登录后管理页面"""
    HomeData = constant_yaml_object.read()['Home']
    login_out, chang_pwd = [value for value in HomeData.values()]

    @pytest.fixture(scope='function', autouse=True)
    def start(self, driver):
        admin_login(driver)
        self.login = Login(driver)
        self.home_page = Home(driver)
        self.home_page.F5()

    @pytest.mark.base_case
    def test_login_out_success(self):
        """测试登录成功后退出"""
        self.home_page.login_out(success=True)
        assert self.login.assert_text_in_source(text_list=TestHomePage.login_out[0]['login_out_success'])

    def test_login_out_fail(self):
        """测试登录成功后取消退出"""
        self.home_page.login_out()
        assert self.home_page.assert_text_in_source(text_list=TestHomePage.login_out[1]['login_out_fail'])

    @pytest.mark.parametrize('old_pwd, new_pwd,expect', [key.values() for key in chang_pwd])
    def test_change_pwd_fail(self, old_pwd, new_pwd, expect):
        """测试修改密码失败"""
        self.home_page.change_pwd(old_pwd, new_pwd)
        assert self.home_page.assert_text_in_source(text_list=expect)


@pytest.mark.base_case
def test_change_pwd_success(driver):
    """测试修改密码成功"""
    user_name = SetUpTestData().create_user[0]
    login = Login(driver)
    home_page = Home(driver)
    login.login(username=user_name, password='Abc123456')

    home_page.change_pwd(old='Abc123456', new='ABc123456')
    assert home_page.assert_text_in_source(text_list=TestHomePage.login_out[0]['login_out_success'])


if __name__ == '__main__':
    pytest.main()