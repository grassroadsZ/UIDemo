# encoding:utf-8
# Motto：good good study, day day up. why you so lazy ？？？
import os

import pytest
import pretty_errors

from settings import reportDir, case_dir

pretty_errors.configure(
    separator_character='*',
    filename_display=pretty_errors.FILENAME_EXTENDED,
    line_number_first=True,
    display_link=True,
    lines_before=5,
    lines_after=2,
    line_color=pretty_errors.RED + '> ' + pretty_errors.default_config.line_color,
    code_color='  ' + pretty_errors.default_config.line_color,
)

def cp_report(path):
    """
    备份报告文件
    :param path: 报告路径
    :return:
    """
    for file in os.listdir(reportDir):
        if file == 'ST_result.html':
            os.renames(os.path.join(reportDir, 'ST_result.html'), os.path.join(reportDir, 'ST_result_bk.html'))

# '--reruns', '1',
# case = '/Users/grassroadsz/Desktop/TarsUIAutoTest/TestCase/TestUI/test_service_manage.py'
case = '/Users/grassroadsz/Desktop/TarsUIAutoTest/TestCase/TestUI/test_login.py'


# case = '/Users/grassroadsz/Desktop/TarsUIAutoTest/TestCase/TestUI/test_home.py'


# 本地调试请指定 --env=local , linux运行请指定--env=linux
def main():
    cp_report(reportDir)
    # , '-vv', '--html=' + reportDir + "/" + currentTime + ".html", '--self-contained-html','--pdb'
    args = ['--env=local',
            # '-vsq',
            '-n=2',
            '--html={}/ST_result.html'.format(reportDir), '--self-contained-html',
            # '--pdb',
            case]
    pytest.main(args)
    # os.system('pip freeze > requirements.txt')

if __name__ == '__main__':
    main()
