# encoding:utf-8
# Motto：good good study, day day up. why you so lazy ？？？

import pytest

from Page.LoginPage import Login
from utils.tools import constant_yaml_object





# @pytest.mark.skip
class TestLogin(object):
    """登录首页"""
    LoginData = constant_yaml_object.read()['Login']
    LoginData = [value.values() for value in LoginData]

    @pytest.fixture(scope='function', autouse=True)
    def start(self, driver):
        self.login_page = Login(driver)
        self.login_page.F5()

    @pytest.mark.base_case
    @pytest.mark.parametrize('user, pwd, expect', LoginData)
    def test_login_success(self, user, pwd, expect):
        """测试登录成功"""
        self.login_page.login(username=user, password=pwd)

        assert self.login_page.assert_text_in_source(expect)


if __name__ == '__main__':
    pytest.main(['-s'])
