# encoding:utf-8
# Motto：good good study, day day up. why you so lazy ？？？


from Page.BasePage import Base
from settings import base_url


class Login(Base):
    """登录页"""
    # 元素对象
    user = ("id", "username")
    pwd = ("id", "password")
    remember_login = ("id", "remember")
    login_button = ("xpath", "//button[@type='submit']")
    user_error = ("xpath", "//div[@class='ant-message-notice-content']")
    login_success = ("css", ".\\_2Z1km1EISPzhl9Djaz6O74 > span")
    login_out_success = ("css", ".ant-message-custom-content > span")

    url = base_url + "#/login"

    def login(self, username: str, password: str):
        """登录流程"""
        self.open_url(Login.url)
        self.input_username(username)
        self.input_password(password)
        self.click_login_button
        self.time_sleep(3)

    def input_username(self, username):
        return self.user_input(Login.user, username)

    def input_password(self, password):
        return self.user_input(Login.pwd, password)

    @property
    def click_login_button(self):
        return self.click(Login.login_button)

    @property
    def get_user_error_info(self):
        value = self.get_text(Login.user_error)
        if value:
            self.log.info("获取登陆失败断言信息:{}".format(value))
            return value

    @property
    def get_login_success_info(self):
        from Page.home.HomePage import Home
        value = self.get_text(Home.account)
        self.log.info("获取登录成功断言信息:{}".format(value))
        return value

    @property
    def login_out_success_info(self):
        return self.get_text(Login.login_out_success)


if __name__ == '__main__':
    pass
