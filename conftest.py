# encoding:utf-8
# Motto：good good study, day day up. why you so lazy ？？？
import pytest
from py._xmlgen import html
from selenium import webdriver

from settings import web_driver_path
from utils.handle_log import MyLog


_driver = None
log = MyLog().out()


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.insert(1, html.th('Test_nodeid'))
    cells.pop()


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(1, html.td(report.nodeid))
    cells.pop()


# 测试失败时添加截图和测试用例描述(用例的注释信息)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """

    pytest_html = item.config.pluginmanager.getplugin('html')
    log.info('{} 开始执行{}的测试用例 {}'.format("*" * 5, item.function.__doc__, "*" * 5))
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            screen_img = _capture_screenshot()
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
        report.description = str(item.function.__doc__)
        report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")





def _capture_screenshot():
    """
    截图保存为base64
    :return:
    """
    return _driver.get_screenshot_as_base64()


def pytest_addoption(parser):
    '''添加命令行参数--env'''
    parser.addoption(
        "--env", action="store", default="local", help="env option:  local or linux"
    )


@pytest.fixture(scope='session', autouse=True)
def driver(request):
    global _driver
    if _driver is None:
        name = request.config.getoption("--env")
        log.info('------------open browser------------')
        if name == "linux":
            selenium_grid_url = "http://127.0.0.1:4444/wd/hub"
            _driver = webdriver.Remote(command_executor=selenium_grid_url,
                                       desired_capabilities={'browserName': 'chrome'})
        else:
            _driver = webdriver.Chrome(executable_path=web_driver_path)

        _driver.implicitly_wait(15)
        # _driver.maximize_window()
        _driver.delete_all_cookies()

    def q():
        _driver.quit()
        # log.info('------------close browser------------')

    request.addfinalizer(q)
    return _driver
