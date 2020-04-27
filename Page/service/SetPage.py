# encoding:utf-8
# Motto：good good study, day day up. why you so lazy ？？？
from Page.home.HomePage import ServiceManage


class Set(ServiceManage):
    """微服务管理-SET管理"""

    # 搜索set名称输入框
    set_search_input = ('xpath', "//input[@placeholder='输入名称']")
    # 搜索按钮
    search_button = ('xpath', "//button[@class='ant-btn']")
    # 具体set的删除按钮
    delete_button = ('link_text', "删除")
    # 创建
    create_button = ('css', "._36GJfl1GVIAmqNSnfYNpet")
    # 点击创建后set名输入框
    set_name = ('id', 'name')
    # 点击创建后set区域输入框
    area_name = ('id', "area")
    # 点击创建后set组输入框
    group_name = ('id', "group")
    # 点击创建后set保存按钮
    save_button = ('xpath', "//button[@type='submit']")

    # 点击删除后确定
    enter_button = ('css', ".ant-btn-danger")

    def create_set(self, name: str, area: str, group: int):
        """创建set"""
        self.click(Set.create_button)
        self.user_input(Set.set_name, name)
        self.user_input(Set.area_name, area)
        self.user_input(Set.group_name, group)
        self.click(Set.save_button)

    def search_set(self, set_name):
        """搜索set"""
        self.search_something([(Set.set_search_input, set_name)], Set.search_button)

    def delete_set(self, set_name):
        """删除set"""
        self.search_set(set_name)
        self.click(Set.delete_button)
        self.click(Set.enter_button)
