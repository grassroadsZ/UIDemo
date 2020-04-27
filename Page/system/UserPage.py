# encoding:utf-8
# Motto：good good study, day day up. why you so lazy ？？？
from Page.home.HomePage import System


class User(System):
    """测试用户管理"""

    # 元素locator

    # 上边框
    search_login_name = ('xpath', "//input[@placeholder='输入登录名']")
    search_name = ('xpath', "//input[@placeholder='输入姓名']")
    search_phone = ('xpath', "//input[@placeholder='输入电话']")
    search_email = ('xpath', "//input[@placeholder='输入邮箱']")

    search_button = ('xpath', "//button[@class='ant-btn']")
    create_button = ('css', '._36GJfl1GVIAmqNSnfYNpet')
    delete_button = ('link_text', '删除')
    edit_button = ('link_text', '编辑')
    reset_pwd_button = ('link_text', '重置密码')

    # 新建
    login_name = ('id', 'user')
    name = ('id', 'name')
    phone = ('id', 'phone')
    email = ('id', 'email')
    description = ('id', 'comments')
    save_button = ('css', ".ant-col-24 > .ant-btn")
    user_create_success = ('xpath', "//div[@class='ant-modal-confirm-body-wrapper']")
    i_know = ('xpath', "//div[@class='ant-modal-confirm-btns']")
    delete_user_success = ('xpath', "//p[@class='ant-empty-description']")

    # 删除
    delete_cancel_button = ('xpath', "//div[@class='ant-modal-confirm-btns']/button[1]")
    delete_enter_button = ('xpath', "//div[@class='ant-modal-confirm-btns']/button[2]")

    def create_user(self, user, name, phone, email, description=None):
        self.click_create_button
        self.user_input(User.login_name, context=user)
        self.user_input(User.name, context=name)
        self.user_input(User.phone, context=phone)
        self.user_input(User.email, context=email)
        self.user_input(User.description, context=description)
        self.click(User.save_button)

    def search_user(self, user, name, phone, email):
        self.search_something(
            locator_text=[(User.search_login_name, user), (User.search_name, name), (User.search_phone, phone),
                          (User.search_email, email)],
            search_locator=User.search_button)

    def delete_user(self, user, name, phone, email, success=False):
        self.search_user(user, name, phone, email)
        self.click(User.delete_button)
        if success:
            self.click(User.delete_enter_button)
            self.time_sleep()
        else:
            self.click(User.delete_cancel_button)
            self.time_sleep()

    def edit_user_info(self, name, phone, email):
        self.click(User.edit_button)
        self.user_input(User.name, context=name)
        self.user_input(User.phone, context=phone)
        self.user_input(User.email, context=email)
        self.user_input(User.description, context='这是编辑用户的测试用例数据')
        self.click(User.save_button)

    @property
    def get_user_create_success_info(self):
        return self.get_text(User.user_create_success)

    @property
    def get_delete_user_success_info(self):
        return self.get_text(User.delete_user_success)

    @property
    def click_create_button(self):
        return self.click(User.create_button)

    @property
    def click_i_know(self):
        return self.click(User.i_know)

    @property
    def click_search_button(self):
        return self.click(User.search_button)
