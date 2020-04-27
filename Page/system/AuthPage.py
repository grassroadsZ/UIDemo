# encoding:utf-8
# Motto：good good study, day day up. why you so lazy ？？？
from Page.home.HomePage import System


class Auth(System):
    """系统管理-权限管理"""

    # 元素locator
    # 应用权限
    app_auth_button = ('xpath', "//span[text()='应用权限']")
    # 服务权限
    service_auth_button = ('xpath', "//span[text()='服务权限']")
    # 用户权限
    user_auth_button = ('xpath', "//span[text()='用户权限']")

    # 应用下拉框
    app_select = ('css', '.ant-select-selection--single')
    # 编辑
    edit_button = ('link_text', "编辑")
    # 用户选择界面
    user_select = ('css', "._2hTQ9O4wle-CA0uLrXEmkR")
    # 添加
    insert_button = ('xpath', "//span[text()='添加']")
    # 移除
    delete_button = ('xpath', "//span[text()='移除']")
    # 保存
    save_button = ('xpath', "//button[contains(.,'保') and contains(.,'存')]")

    def edit_app_auth(self, user, insert=True):
        """编辑app权限:默认添加"""
        self.click_select_li(Auth.app_select, text='UIAuto')
        self.click(Auth.edit_button)
        self.click_select_li(Auth.user_select, user)
        self.double_click(Auth.insert_button if insert else Auth.delete_button)
        self.double_click(Auth.save_button)
