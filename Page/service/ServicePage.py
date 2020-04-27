# encoding:utf-8
# Motto：good good study, day day up. why you so lazy ？？？
from Page.home.HomePage import ServiceManage
from utils.tools import SetUpTestData, TearDownTestData


class Service(ServiceManage):
    """服务管理"""
    app_name = ('xpath', "//input[@placeholder='输入应用名']")
    service_name = ('xpath', "//input[@placeholder='输入服务名']")

    search_button = ('xpath', "//button[@class='ant-btn']")
    reset_button = ('xpath', "//button[2]/span")
    create_button = ('css', ".\\_36GJfl1GVIAmqNSnfYNpet")
    select_app_button = ('xpath', "//div[@class='ant-select-selection-selected-value' and @title='--请选择应用--']")

    service_name_input = ('xpath', "//input[@placeholder='服务名']")
    save_button = ('xpath', "//div[@class='_1bA4h4_uh2oRf5Jerb_iPC']/button")

    delete_button = ('link_text', '删除')
    delete_cancel_button = ('xpath', "//div[@class='ant-modal-confirm-btns']/button[1]")
    delete_enter_button = ('xpath', "//div[@class='ant-modal-confirm-btns']/button[2]")

    create_instance_button = ('link_text', '创建实例')
    deployment_name = ('id', "deployment_name")
    docker_image_name = ('id', 'docker_image')
    next_step = ('css', '._1tiarB9DWjJmYyVmuD5QWH')
    servant_setting_button = ('css', "div:nth-child(1) > .ant-btn-primary")
    obj_name = ('id', 'servant_name')
    port = ('id', 'port')
    servant_save_button = ('xpath', "//button[@type='submit']")
    xia_yi_bu = ('css', '.\\_1tiarB9DWjJmYyVmuD5QWH')

    def create_service(self, service_name):
        """
        创建服务
        :param service_name: type:str
        :return:
        """
        self.click_create
        self.click_select_li(Service.select_app_button, 'UIAuto')
        self.user_input(Service.service_name_input, service_name)
        self.click(Service.save_button)

    def search_create_service_success(self, service_name):
        """
        服务创建成功后的服务
        :param service_name:
        :return:
        """
        self.search_something(locator_text=[(Service.app_name, 'UIAuto'), (Service.service_name, service_name)],
                              search_locator=Service.search_button)

    def delete_service(self, name):
        """
        删除服务
        :param name:要删除的service_name
        :return:
        """
        self.search_create_service_success(name)
        self.click_delete_button
        self.click(Service.delete_enter_button)

    instance_service_name = SetUpTestData().create_instance_service

    def create_instance(self, instance_name, image_name, port):
        self.search_create_service_success(service_name=Service.instance_service_name)
        self.click(Service.create_instance_button)
        self.user_input(Service.deployment_name, instance_name)
        self.user_input(Service.docker_image_name, image_name)
        self.click_next_setp
        self.click_servant_setting
        self.user_input(Service.obj_name, context=instance_name)
        self.user_input(Service.port, context=port)
        self.click_servant_save_button
        self.click_xia_yi_bu_button
        self.click_xia_yi_bu_button
        self.click_xia_yi_bu_button

    @staticmethod
    def delete_instance_service():
        TearDownTestData().delete_service(Service.instance_service_name)

    @property
    def click_create(self):
        self.click(Service.create_button)

    @property
    def click_search(self):
        self.click(Service.search_button)

    @property
    def click_delete_button(self):
        self.click(Service.delete_button)

    @property
    def click_next_setp(self):
        self.click(Service.next_step)

    @property
    def click_servant_setting(self):
        self.click(Service.servant_setting_button)

    @property
    def click_servant_save_button(self):
        self.click(Service.servant_save_button)

    @property
    def click_xia_yi_bu_button(self):
        self.double_click(Service.xia_yi_bu)
