# encoding:utf-8
# Motto：good good study, day day up. why you so lazy ？？？
import os

import pytest

from settings import reportDir, case_dir
from utils.handle_thread import MyThread
from utils.tools import SetUpTestData, log


# 本地调试请指定 --env=local , linux运行请指定--env=linux
def main():
    SetUpTestData.cp_report(reportDir)

    # 生成参数化的数据到yaml文件
    log.info('开始测试数据生成')
    SetUpTestData().yaml_to_case_data(random_gen=True)

    args = ['--env=linux', '--alluredir=./allure_report',
            '--reruns', '1',
            '-vsq',
            '-n=4',
            '--html={}'.format(os.path.join(reportDir, 'ST_result.html')), '--self-contained-html', case_dir]

    pytest.main(args)
    log.info('开始测试数据清理')
    args_dict = {"get_application_list": "get", "get_server_list": "post", "get_set_list": "get", "list_user": 'post'}
    MyThread(MyThread.get_delete_data(args_dict)).before_start_delete_data(args_dict)


if __name__ == '__main__':
    main()