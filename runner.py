# -*- coding: utf-8 -*-
"""
@Time ： 2025/8/14 11:03
@Auth ： 张冠
@Function ：请输入模块功能描述
"""
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

from cases.exceptions_case import ExceptionsTestCase
from common.common_utils import CommonUtils
from keywords.web_keys import Web
from cases.login_case import LoginTestCase


def run_login_tests(browser="chrome"):
    # 初始化浏览器驱动
    if browser.lower() == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    elif browser.lower() == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    else:
        raise ValueError(f"不支持的浏览器: {browser}")

    try:
        # 初始化工具类和页面操作类
        utils = CommonUtils()
        web = Web(driver, utils)

        # 初始化测试用例并执行
        login_tests = LoginTestCase(web, utils)

        # 执行登录用例
        # login_tests.test_positive_login()
        # login_tests.test_negative_username()
        # login_tests.test_negative_password()

        # 执行异常测试用例
        print("\n===== 开始执行异常测试用例 =====")
        exceptions_tests = ExceptionsTestCase(web, utils)
        exceptions_tests.run_all_exceptions_tests()

        print("所有测试用例执行完成，未发现异常")

    except AssertionError as ae:
        print(f"测试断言失败: {str(ae)}")
        if 'utils' in locals() and 'driver' in locals():
            utils.take_screenshot(driver, f"断言失败_{str(ae)[:30]}")
    except Exception as e:
        print(f"执行过程中发生错误: {str(e)}")
        if 'utils' in locals() and 'driver' in locals():
            utils.take_screenshot(driver, f"执行错误_{str(e)[:30]}")
    finally:
        # 确保浏览器关闭
        if 'driver' in locals():
            driver.quit()
        # 生成测试报告
        if 'utils' in locals():
            utils.generate_html_report()


if __name__ == "__main__":
    # 可选择浏览器: "chrome" 或 "firefox"
    run_login_tests(browser="firefox")
