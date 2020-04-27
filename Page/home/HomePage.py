# encoding:utf-8
# Motto：good good study, day day up. why you so lazy ？？？

from Page.BasePage import Base


class Home(Base):
    """登录成功后的页面"""

    # 右侧页面元素
    account = ("xpath", "//div[@class='_1TgnsYN4FJaF4jHm0Wel-k']/div/span[2]")
    logout_out_button = ('xpath', '//*[contains(text(), "退出登录")]')
    reset_pwd_button = ('xpath', '//*[contains(text(), "密码修改")]')

    # 修改密码页面
    old_pwd = ('id', "form_in_modal_old_passwd")
    new_pwd = ('id', "form_in_modal_new_passwd")
    check_new_pwd = ('id', 'form_in_modal_check_passwd')
    change_pwd_enter_button = ('xpath', "//div[@class='ant-modal-footer']/div/button[2]")
    change_pwd_cancel_button = ('xpath', "//button[@class='ant-btn']")

    # 退出登录
    login_out_cancel_button = ('xpath', "//div[@class='ant-modal-confirm-btns']/button[1]")
    login_out_enter_button = ('xpath', "//div[@class='ant-modal-confirm-btns']/button[2]")

    # 左侧侧边栏页面元素
    Micro_service_manage_button = ('xpath', "//span[text()='微服务管理']")
    system_manage_button = ('xpath', "//span[text()='系统管理']")

    @property
    def click_Micro_service_manage(self):
        return self.click(Home.Micro_service_manage_button)

    @property
    def click_system_manage(self):
        return self.click(Home.system_manage_button)

    def change_pwd(self, old, new, success=True):
        self.click(Home.account)
        self.click(Home.reset_pwd_button)
        self.user_input(Home.old_pwd, context=old)
        self.user_input(Home.new_pwd, context=new)
        self.user_input(Home.check_new_pwd, context=new)
        if success:
            self.click(Home.change_pwd_enter_button)
        else:
            self.click(Home.change_pwd_cancel_button)

    def login_out(self, success=False):
        """退出登录,默认不退出"""
        self.move_to_element(Home.account)
        self.click(Home.account)
        self.click(Home.logout_out_button)
        if success:
            self.click(Home.login_out_enter_button)
        else:
            self.click(Home.login_out_cancel_button)


class ServiceManage(Home):
    """微服务管理展开页面"""
    application_manage_button = ('link_text', "应用管理")
    service_manage_button = ('link_text', "服务管理")
    set_manage_button = ('link_text', "SET管理")

    @property
    def click_service_manage(self):
        return self.click(ServiceManage.service_manage_button)

    @property
    def click_app_manage(self):
        return self.click(ServiceManage.application_manage_button)

    @property
    def click_set_manage(self):
        return self.click(ServiceManage.set_manage_button)


class System(Home):
    """系统管理展开页面"""
    user_manage_button = ('link_text', "用户管理")
    auth_manage_button = ('link_text', "权限管理")

    @property
    def click_user_manage(self):
        return self.click(System.user_manage_button)

    @property
    def click_auth_manage(self):
        return self.click(System.auth_manage_button)
