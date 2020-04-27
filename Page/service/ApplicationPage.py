# encoding:utf-8
# Motto：good good study, day day up. why you so lazy ？？？
from Page.home.HomePage import ServiceManage


class Application(ServiceManage):
    """应用管理页面"""
    search_app_input = ('xpath', "//input[@placeholder='输入应用名']")
    search_button = ('xpath', "//button[@class='ant-btn']")
    reset_button = ('xpath', "//button[2]/span")
    create_button = ('css', ".\\_36GJfl1GVIAmqNSnfYNpet")

    app_name = ('id', 'name')
    description = ('id', "description")
    save = ('css', ".ant-form-item-children > .ant-btn")

    delete_button = ('link_text', '删除')
    delete_cancel_button = ('xpath', "//div[@class='ant-modal-confirm-btns']/button[1]")
    delete_enter_button = ('xpath', "//div[@class='ant-modal-confirm-btns']/button[2]")

    def create_app(self, name, text):
        self.click_create
        self.input_app_name(name)
        self.input_app_description(text)
        self.click_save_button

    def delete_app(self, name):
        self.search_app(name)
        self.click_delete_button
        self.click(Application.delete_enter_button)

    def search_app(self, name):
        self.search_something(locator_text=[(Application.search_app_input, name)],
                              search_locator=Application.search_button)

    def input_app_name(self, name):
        return self.user_input(Application.app_name, name)

    def input_app_description(self, text=' '):
        return self.user_input(Application.description, text)

    @property
    def click_save_button(self):
        self.click(Application.save)

    @property
    def click_create(self):
        self.click(Application.create_button)

    @property
    def click_search(self):
        self.click(Application.search_button)

    @property
    def click_reset(self):
        self.click(Application.reset_button)

    @property
    def click_delete_button(self):
        self.double_click(Application.delete_button)
