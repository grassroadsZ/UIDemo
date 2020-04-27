# encoding:utf-8
# Motto：good good study, day day up. why you so lazy ？？？
import time

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from settings import base_url, Retry_count
from utils.handle_log import MyLog

# 定位器字典 把value打包
locatorTypeDict = {
    'xpath': By.XPATH,
    'css': By.CSS_SELECTOR,
    'id': By.ID,
    'name': By.NAME,
    'className': By.CLASS_NAME,
    'tagName': By.TAG_NAME,
    'link': By.LINK_TEXT,
    'parLink': By.PARTIAL_LINK_TEXT
}


class Base(object):
    """基于原生的selenium做二次封装"""

    # 默认等待2s,更符合真实的操作
    time_wait = 2

    def __init__(self, driver):
        self.driver = driver

        # 默认轮训最长时间，隐式等待设置的为15s
        self.time = 10
        # 默认轮训间隔时间
        self.t = 0.25

        self.log = MyLog().out()
        self.base_url = base_url

    def start(self, url, _url):
        """
        不拉起浏览器打开网页
        :param url: 打开网页
        :param _url: 期望网页
        :return:
        """
        self.driver.get(url)
        self._get_current_url(_url)

    def open_url(self, url):
        self.driver.get(url)
        self.log.info('正在打开网址：{}'.format(url))

    def assert_title(self, titleText):
        """
        页面标题上是否包含关键字,支持传入多个参数
        :param titleStr: 关键字
        :param args: 支持传入多个参数
        :return:布尔
        """
        try:
            assert titleText in self.driver.title, \
                "在title里没有找到%s" % titleText
            self.log.info("加载网页正确")  # 业务self.assertTrue()
            return True
        except Exception as error:
            self.log.error(error)
            return False

    def assert_text_in_source(self, text_list) -> bool:
        """
        网页源码是否包含关键字 做业务判断
        :param text_list: list [arg1,arg2...]
        :return:True/False
        """
        if type(text_list) == str:
            text_list = text_list.split()
        n = 0
        while n < 10:
            if next(iter(text_list)) in self.driver.page_source:
                self.log.info(" %s 包含在page_source" % text_list)
                return True
            self.time_sleep(0.5)
            n += 1

        self.log.info("%s 未包含在page_source" % text_list)
        return False

    def time_sleep(self, time_wait=2):
        """
        强制等待默认为2秒
        :param time_wait:
        :return:
        """
        if time_wait <= 0:
            time.sleep(time_wait)
        else:
            # self.log.info("等待%ss" % time_wait)
            time.sleep(time_wait)

    def max_size(self):
        """
        放大浏览器最大化 需要先拉起浏览器
        :return:
        """
        time.sleep(0.5)  # 切换展示
        self.driver.maximize_window()

    def set_size(self, width=800, height=600):
        """
        先打印浏览器尺寸，设置浏览器到尺寸
        :param width: 宽
        :param height: 高
        :return:
        """
        self.driver.set_window_size(width, height, windowHandle="current")  # 当前句柄
        self.log.info("width:{},height:{} 尺寸设置成功".format(width, height))

    def _get_current_url(self, expect_url):
        try:
            assert expect_url == self.driver.current_url
        except Exception as error:
            self.log.info(error)

    def F5(self):
        """
        刷新后验证网页正确
        :return:
        """
        self.driver.refresh()
        self.log.info("F5刷新完毕")
        self.time_sleep()

    def back(self, current_url, time_wait=4):
        """
        后退到之前的页面（等同浏览器上按回退按钮）
        条件：先需要有前后打开的2个页面
        :param current_url:形参是验证当前页面
        :param time_wait:属于time_sleep方法
        :return:
        """
        self.time_sleep(time_wait)
        self.driver.back()
        self._get_current_url(current_url)
        self.log.info("back网页成功")

    def forward(self, current_url, time_wait=4):
        """
        配合浏览器回退使用，回到之前的页面
        :param current_url:形参是验证当前页面
        :param time_wait:属于time_sleep方法
        :return:
        """
        self.time_sleep(time_wait)
        self.driver.forward()
        self._get_current_url(current_url)
        self.log.info("forward网页成功")

    def get_element(self, locator: tuple):
        """非显示等待定位元素，返回元素对象，未定位到，抛出Timeout异常"""
        if not isinstance(locator, tuple):
            self.log.info(f"{locator}参数类型错误，必须为元祖类型:locator=('id','value')")
        by = locator[0]
        value = locator[1]
        self.log.info("正在使用 {} 定位方式定位元素：{}".format(by, value))
        n = 0

        while n < Retry_count:

            if by == "id":
                element = self.driver.find_element_by_id(value)
            elif by == "name":
                element = self.driver.find_element_by_name(value)
            elif by == "class":
                element = self.driver.find_element_by_class_name(value)
            elif by == "link_text":
                element = self.driver.find_element_by_link_text(value)
            elif by == "xpath":
                element = self.driver.find_element_by_xpath(value)
            elif by == "css":
                element = self.driver.find_element_by_css_selector(value)
            elif by == "tag_name":
                element = self.driver.find_element_by_tag_name(value)
            else:
                self.log.error("{}定位方式不在可支持范围内".format(by))
                raise NameError(
                    "不在选择范围内,'id','name','class','link_text','xpath','css','tag'.")
            if isinstance(element, WebElement):
                self.time_sleep(0.5)
                return element
            else:
                self.time_sleep(0.5)
                n += 1
                continue



    def get_element_wait(self, locator, timeout=12, poll=0.5):
        '''
        单个元素的显式等待，接收参数更少（可以不直接使用）
        driver.element_wait("css=>#el", 10)
        :param xpath:
        :param poll:不填写则默认0.5秒
        :param timeout:默认12秒
        '''

        if not isinstance(locator, tuple):
            self.log.info(f"{locator}参数类型错误，必须为元祖类型:locator=('id','value')")

        by = locator[0]
        value = locator[1]
        n = 0
        while n < Retry_count:
            self.log.info("正在使用 {} 定位方式定位value值为 {} 的元素".format(by, value))
            if by == "id":
                element = WebDriverWait(self.driver, timeout, poll).until(
                    EC.presence_of_element_located((By.ID, value)))
            elif by == "name":
                element = WebDriverWait(self.driver, timeout, poll).until(
                    EC.presence_of_element_located((By.NAME, value)))
            elif by == "class":
                element = WebDriverWait(self.driver, timeout, poll).until(
                    EC.presence_of_element_located((By.CLASS_NAME, value)))
            elif by == "link_text":
                element = WebDriverWait(self.driver, timeout, poll).until(
                    EC.presence_of_element_located((By.LINK_TEXT, value)))
            elif by == "xpath":
                element = WebDriverWait(self.driver, timeout, poll).until(
                    EC.presence_of_element_located((By.XPATH, value)))
            elif by == "css":
                element = WebDriverWait(self.driver, timeout, poll).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, value)))
            elif by == "tag":
                element = WebDriverWait(self.driver, timeout, poll).until(
                    EC.presence_of_element_located((By.TAG_NAME, value)))
            else:
                raise NameError("不在选择范围内,'id','name','class','link_text','xpath','css','tag'.")
            if isinstance(element, WebElement):
                return element
            else:
                self.time_sleep(0.5)
                n += 1
                continue

    def get_elements_wait(self, locator, timeout=12, poll=0.5):
        '''
        单个元素的显式等待，接收参数更少（可以不直接使用）
        driver.element_wait("css=>#el", 10)
        :param xpath:
        :param poll:不填写则默认0.5秒
        :param timeout:默认12秒
        '''

        if not isinstance(locator, tuple):
            self.log.info(f"{locator}参数类型错误，必须为元祖类型:locator=('id','value')")

        by = locator[0]
        value = locator[1]
        self.log.info("正在使用 {} 定位方式定位value值为 {} 的一组元素".format(by, value))
        n = 0

        while n < Retry_count:
            if by == "id":
                element = WebDriverWait(self.driver, timeout, poll).until(
                    EC.presence_of_element_located((By.ID, value)))
            elif by == "name":
                element = WebDriverWait(self.driver, timeout, poll).until(
                    EC.presence_of_element_located((By.NAME, value)))
            elif by == "class":
                element = WebDriverWait(self.driver, timeout, poll).until(
                    EC.presence_of_element_located((By.CLASS_NAME, value)))
            elif by == "link_text":
                element = WebDriverWait(self.driver, timeout, poll).until(
                    EC.presence_of_element_located((By.LINK_TEXT, value)))
            elif by == "xpath":
                element = WebDriverWait(self.driver, timeout, poll).until(
                    EC.presence_of_element_located((By.XPATH, value)))
            elif by == "css":
                element = WebDriverWait(self.driver, timeout, poll).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, value)))
            elif by == "tag":
                element = WebDriverWait(self.driver, timeout, poll).until(
                    EC.presence_of_element_located((By.TAG_NAME, value)))
            else:
                raise NameError("不在选择范围内,'id','name','class','link_text','xpaht','css','tag'.")
            if isinstance(element, WebElement):
                self.time_sleep(1)
                return element
            else:
                n += 1
                self.time_sleep(0.5)
                continue

    def get_window_handle(self):
        """
        网页句柄
        :param num:
        :return:
        """
        handles = self.driver.window_handles
        return handles

    def leave_frame(self):
        """
        将焦点切换到默认框架(iframe)
        """
        self.driver.switch_to.default_content()

    def submit(self, locator):
        """
        提交
        driver.submit("xpath=>value")
        """
        self.time_sleep(self.time_wait)
        self.get_element_wait(locator)  # 显式等待
        self.get_element(locator).submit()  # 当显示等待触发后在提交
        self.log.info('确认元素%s后提交了' % locator)

    def js_execute(self, script, *args):
        """
        执行js脚本  *args为不定长 元祖
        使用方法：
        driver.js("window.scrollTo(200,1000);")
        """
        self.driver.execute_script(script, *args)
        self.log.info('Execute script: %s' % (script))

    def check_element(self, locator, text):
        """
        定位检查后在输出
        :Usage:
        driver.check_element("xpath,//*[@id='el']"), "selenium")
        """
        self.get_element(locator)  #
        el = self.get_element_wait(locator)  # 双保险
        try:
            if el: el.clear()
        except:
            self.log.error('clear failed is %s' % locator)
        el.send_keys(text)
        time.sleep(1)
        print('check 元素%s is %s' % (text, locator))

    def click(self, locator):
        """
        点击页面元素
        """
        if self.get_element_wait(locator):
            el = self.get_element_wait(locator)
        else:
            el = self.get_element(locator)
        self.time_sleep(0.5)
        self.log.info("点击 {}".format(el.text))
        el.click()

    def user_input(self, locator, context):
        '''
        输入内容
        :param pattern: 元素定位方法，id，name等
        :param position: 定位元素的value
        :param context: 要输入的内容
        :return:
        '''
        try:
            element = self.get_element(locator)
            element.clear()
            element.send_keys(context)
            self.time_sleep(1)
            self.log.info(f"输入框内输入{context}")
        except Exception as error:
            self.log.error(error)

    def user_input_clear(self, locator_list):
        """
        清空输入框
        :param locator: 元素表达式
        :return:
        """
        try:
            if isinstance(locator_list, list):
                for locator in locator_list:
                    ele = self.get_element(locator)
                    ele.clear()
            else:
                ele = self.get_element(locator_list)
                ele.clear()
            self.log.info("输入框以清空")
        except Exception as error:
            self.log.error("清空输入框错误，{}".format(error))

    def get_window_handle(self):
        """
        返回当前网页句柄
        :return:
        """
        return self.driver.current_window_handle

    def click_partial(self, text):
        """
        可以局部也可以全局
        driver.click_text("新闻")
        """
        self.time_sleep(self.time_wait)
        self.driver.find_element_by_partial_link_text(text).click()
        self.log.info('打开%s link' % text)

    def double_click(self, locator):
        """
        双击元素
        driver.double_click(("xpath",'name'))
        """
        if self.get_element_wait(locator):
            el = self.get_elements_wait(locator)
        else:
            el = self.get_element(locator)
        ActionChains(self.driver).double_click(el).perform()
        print('双击元素:', locator)

    def get_attribute(self, xpath, value):
        """
        拿到元素属性
        driver.get_attribute("xpath=>定位器", "type")
        """
        self.time_sleep(self.time_wait)
        self.get_element_wait(xpath)
        ele = self.get_element(xpath)
        attr_value = ele.get_attribute(value)  # get_attribute是API  attr元素el的属性
        if attr_value:
            self.log.info('attribute_value %s is: %s' % (value, attr_value))
            return attr_value
        else:
            self.log.error('not found attribute_value: %s' % value)
            return None  # 布尔

    def get_link_text(self, locator):
        '''
        获取元素内容 注意并不是所有的元素都会有text
        driver.get_link_text("link=>value")
        :param pattern: 鼓励只用超文本的
        :param position: 定位元素的value
        :return:
        '''
        try:
            element = self.get_element(locator)
            text = element.text
            return text
        except Exception as error:
            self.log.error(error)

    def switch_frame(self, locator=None):
        """
        切换iframe
        :param locatValue: 框架元素
        :return:
        """
        if locator:
            self.driver.switch_to.frame(locator)

    def frame_to_switch(self, target, locator, timeout=10):
        """
        显式等待，判断是否需要切换到frame
        :param driver:其他函数的
        :param targetType:用字典的
        :param locatorValue:
        :return:
        """
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until(EC.frame_to_be_available_and_switch_to_it
                       ((locatorTypeDict[target.lower()], locator)))
            self.log.info("frame存在，切换成功")
        except Exception as error:
            self.log.error(error)

    def switch_accept_alert(self):
        """
        确认弹出窗体
        driver.accept_alert()
        """
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        """
        关闭弹出窗体 拒绝
        driver.dismiss_alert()
        """
        self.driver.switch_to.alert.dismiss()

    def isSelected(self, locator: tuple):
        """判断元素是否被选中，返回bool值"""
        ele = self.get_element(locator)
        r = ele.is_selected()
        return r

    def isElementExis(self, locator: tuple):
        """判断元素是否存在，返回True或是False"""
        try:
            self.get_element(locator)
            return True
        except:
            return False

    def is_alert(self, timeout=3):
        """是否为alert弹窗"""
        try:
            result = WebDriverWait(self.driver, timeout, self.t).until(EC.alert_is_present())
            return result
        except:
            return False

    def get_alert_text(self) -> str:
        """
        get test of alert
        :return: text of alert
        """
        alert = self.is_alert()
        if alert:
            return alert.text
        else:
            self.log.error("获取alert文本失败")
            raise NoAlertPresentException("没有alert抛出")

    def get_text(self, locator):
        """获取文本"""
        try:
            t = self.get_element_wait(locator, poll=0.2).text
            self.log.info(f"获取文本内容{t}成功")
            return t
        except:
            self.log.error("获取文本内容失败")
            return None

    def js_focus_element(self, locator):
        """聚焦元素"""
        target = self.get_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)

    def js_roll_top(self):
        """滚动至进度条顶部"""
        js = "windows.scrollTo(0,0)"
        self.driver.execute_script(js)
        self.log.info("滚动进度条至顶部")

    def js_roll_end(self, x=0):
        """滚动至进度条底部"""
        js = f"windows.scrollTo({x},document.body.scrollHeight)"
        self.driver.execute_script(js)
        self.log.info("滚动进度条至底部")

    def select_by_index(self, locator, index=0):
        """通过索引选择，默认选择0个"""
        ele = self.get_element(locator)
        Select(ele).select_by_index(index)
        # self.log.info(f"通过索引为{index} 选择 {ele.text}")

    def select_by_value(self, locator, value: str):
        """通过value选择"""
        ele = self.get_element(locator)
        Select(ele).select_by_value(value)
        # self.log.info(f"通过索引为{index} 选择 {ele.text}")

    def select_by_text(self, locator, text: str):
        """通过text文本选择"""
        ele = self.get_element(locator)
        Select(ele).select_by_visible_text(text)

    def switch_handle(self, window_name):
        """切换窗口"""
        self.driver.switch_to.window(window_name)
        self.log.info("切换窗口成功")

    def switch_alert(self):
        """移至alert弹窗"""
        if not self.is_alert():
            self.log.error("alert不存在")
        else:
            return self.is_alert()

    def move_to_element(self, locator=("css", "body")):
        """鼠标悬停操作"""
        ele = self.get_element(locator)

        if ele.text:
            self.log.info(f"鼠标移动至元素{ele.text}")
        ActionChains(self.driver).move_to_element(ele)
        self.time_sleep(1)
        ActionChains(self.driver).perform()

    def click_select_li(self, locator, text):
        """
        点击div及li组成的select选项框
        :param locator: div组成的select选择框的位置
        :param text: select框里面的内容
        :return:
        """
        self.click(locator)
        self.click(("xpath", "//li[contains(.,'{}')]".format(text)))

    def search_something(self, locator_text: list, search_locator):
        """
        搜索需要内容是否出现，用于检查接口创建的数据在前端存在延时情况,locators中的定位表达式需要与texts中的输入一一对应
        :param locators: [(定位表达式,输入文本文本)]嵌套元祖的列表
        :param search_locator: 搜索输入框的表达式
        :return:
        """
        n = 0
        # 需要修改为必须传入的是序列类型
        while n < Retry_count:
            self.F5()
            # 多个搜索框进行输入搜索
            for locator in locator_text:
                self.user_input(locator[0], locator[1])
            self.click(search_locator)
            # 将输入的内容进行清空
            for locator in locator_text:
                self.user_input_clear(locator[0])
            self.time_sleep()
            if self.assert_text_in_source(list([locator[1] for locator in locator_text])):
                break
            n += 1
            continue



if __name__ == '__main__':
    driver = webdriver.Chrome()
    web = Base(driver)
    driver.get("http://www.grassroadsz.top")
    loc = ("id", "navMenu")
    t = web.get_text(loc)
    print(t)
