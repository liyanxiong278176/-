import time

import pytest

from base.apiutil import Api
from common.dingRobot import send_dingding_message
from common.readyaml import ReadAndWriteYaml, get_yaml

read=ReadAndWriteYaml()
@pytest.fixture(scope="session",autouse=True)
def clear_extract():
    read.clear_extract_yaml_data()

@pytest.fixture(scope="session",autouse=True)
def function(request):
    print("-------------------------------接口测试开始--------------------------------------")
    yield
    print("------------------------------接口测试结束----------------------------------------")


@pytest.fixture(scope="session",autouse=True)
def login():
    login_data=get_yaml("./testcase/Login/login.yaml")
    # print("login_data",login_data)
    # print("login_data",login_data[0][0])
    # print("login_data",login_data[0][1])
    Api().specification_yaml(login_data[0][0],login_data[0][1])


def pytest_terminal_summary(terminalreporter,exitstatus, config):
    """
    在conftest文件中
    pytest内置钩子函数，函数名为固定写法，不可变更
    每次pytest测试完成后，自动化收集测试结果都数据
    :param terminalreporter: 内部终端报告对象，对象是stats
    :param exitstatus: 将报告回操作系统的退出状态
    :param config: pytest配置对象
    :return:
    """
    # 测试用例总数
    case_total = terminalreporter._numcollected
    # 测试通过数
    case_pass = len(terminalreporter.stats.get("passed", []))
    # 测试失败数
    case_fail = len(terminalreporter.stats.get("failed", []))
    # 测试错误数
    case_error = len(terminalreporter.stats.get("error", []))
    # 测试跳过数
    case_skip = len(terminalreporter.stats.get("skipped", []))
    # 测试用例执行时间
    # duration = time.time() - terminalreporter.sessionstarttime
    # print("执行时间：%s" % duration)
    content=f"""
    自动化测试报告
    测试用例总数:{case_total}
    测试通过数：{case_pass}
    测试失败数：{case_fail}
    测试错误数:{case_error}
    测试跳过数：{case_skip}
    接口报告地址： www.baidu.com
    """

    send_dingding_message(content, True)


