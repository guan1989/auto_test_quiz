# -*- coding: utf-8 -*-
"""
@Time ： 2025/8/14 20:50
@Auth ： 张冠
@Function ：请输入模块功能描述
"""
import os
import time
from time import sleep

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, ElementNotInteractableException, \
    StaleElementReferenceException, InvalidElementStateException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from common.Logger import logger


class Web:
    def __init__(self):
        self.driver: webdriver.Edge = None
        # 关联字典
        self.relations_dict = {}

    def open_browser(self, browser: str = 'edge'):
        """

        :param browser:默认Edge;gc-谷歌
        :return:
        """
        if browser == 'edge':
            edge_options = Options()
            pre_fs = {
                "credentials_enable_service": False,  # 禁用密码服务
                "profile.password_manager_enabled": False  # 禁用密码管理器
            }
            edge_options.add_experimental_option("prefs", pre_fs)
            # 禁用自动化控制标识
            edge_options.add_argument("--disable-blink-features=AutomationControlled")
            edge_options.add_argument("--disable-extensions")
            edge_options.add_argument("--disable-popup-blocking")
            edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            edge_options.add_experimental_option('useAutomationExtension', False)

            self.driver = webdriver.Edge(options=edge_options)
        else:
            option = webdriver.ChromeOptions()
            # 不自动关闭浏览器的配置
            option.add_experimental_option("detach", True)
            # 在打开浏览器之前，去掉自动化标识
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            option.add_argument('--disable-blink-features=AutomationControlled')

            ##关掉密码弹窗
            prefs = {}
            prefs['credentials_enable_service'] = False
            prefs['profile.password_manager_enabled'] = False
            option.add_experimental_option('prefs', prefs)
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # chrome 浏览器版本：139.0.7258.67（正式版本） （64 位）
            driver_path = os.path.join(project_root, "lib", "chromedriver.exe")
            self.driver = webdriver.Chrome(options=option, service=Service(driver_path))
        # 隐式等待
        self.driver.implicitly_wait(5)
        # 最大化
        self.driver.maximize_window()

    def geturl(self, url: str = ''):
        """
        打开网站
        :param url: 网站地址，一定要http开头
        :return:
        """
        # 这个是兼容非http开头的url写法
        if not url.startswith('http'):
            url = 'http://' + url

        self.driver.get(url)

    def __find_ele(self, lo: str = ''):
        """
        xpath一般是/
        id一般是纯英文单词
        :param lo: 定位表达式，支持xpath，id,name
        :return: 返回找到元素，如果没找到就报错
        """
        try:
            if lo.startswith('/'):
                ele = self.driver.find_element('xpath', lo)
            elif lo.startswith('$'):
                name_value = lo[1:]  # 去掉前缀$
                ele = self.driver.find_element('name', name_value)
            elif lo.startswith('link_test'):
                name_value = lo[9:]  # 去掉前缀
                # ele = self.driver.find_element('LINK_TEXT', name_value)
                ele = self.driver.find_element(By.LINK_TEXT, name_value)
            else:
                ele = self.driver.find_element('id', lo)
            # 操作元素高亮
            if ele:
                self.driver.execute_script("arguments[0].style.background = '#4aff00'", ele)
            return ele
        except NoSuchElementException as e:
            raise AssertionError(f"[NoSuchElement] 元素定位失败: {lo}") from e

    def input(self, lo: str = '', value: str = "", ):
        """
        往元素里面输入
        :param value: 要输入的值
        :param lo: 定位表达式，支持xpath，id
        :return:
        """
        try:
            ele = self.__find_ele(lo)
            ele.send_keys(value)
        except InvalidElementStateException as e:
            raise AssertionError(f"[InvalidState] 元素状态无效: {lo}") from e
        except ElementNotInteractableException  as e:
            raise AssertionError(f"[ElementNotInteractable] 元素不可输入: {lo}") from e

    def clear(self, lo: str = ''):
        """
        清除文本
        :param lo:定位表达式
        :return:
        """
        ele = self.__find_ele(lo)
        ele.clear()

    def click(self, lo: str = ''):
        """
        点击元素
        :param lo: 定位表达式，支持xpath，id
        :return:
        """
        try:
            ele = self.__find_ele(lo)
            ele.click()
        except ElementNotInteractableException as e:
            raise AssertionError(f"[ElementNotInteractable] 元素不可交互: {lo}") from e
        except StaleElementReferenceException as e:
            raise AssertionError(f"[StaleElement] 元素已失效: {lo}") from e

    def quit(self):
        """关闭浏览器"""
        self.driver.quit()
        self.driver = None

    def assert_text(self, lo: str = '', expected_text: str = ''):
        """
        断言文本
        :param timeout: 等待时间
        :param expected_text: 期望值
        :param lo: 定位表达式
        :return:
        """
        try:
            # 获取定位器元组
            loc = self.__find_ele(lo)
            actual_text = loc.text
            if expected_text == actual_text:
                return True
            else:
                raise AssertionError(f"按键存但与预期值不符。预期值: {expected_text},实际值：{actual_text}")
        except Exception as e:
            raise AssertionError(f"验证文本失败: {str(e)}")

    def assert_url(self, expected: str):
        """
        断言当前URL
        :param expected: 预期值
        :return: 成功True，失败就抛异常
        """
        current_url = self.driver.current_url
        logger.info(f'断言，实际结果：{current_url}   --- 期望值：{expected}')
        if current_url.__contains__(expected):
            return True
        else:
            assert current_url.__contains__(expected)

    def assert_button(self, lo: str = '', expected_text: str = '', timeout: int = 10):

        # 获取定位器元组
        loc = self.__find_ele(lo)
        # 校验按键文本
        actual_text = loc.text
        if expected_text == actual_text:
            return True
        else:
            raise AssertionError(f"按键存但与预期值不符。预期值: {expected_text},实际值：{actual_text}")

    def assert_element(self, lo: str = ''):
        # 获取定位器元组
        locator = (By.ID, lo)
        try:
            # 显式等待3秒，直到元素可见
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            raise AssertionError(f"元素 {lo} 在3秒内未可见")

    def sleep(self, t: str):
        try:
            t = float(t)
        except:
            # 如果转失败，就说明输入的不是一个数字
            # 默认就按等待1s
            t = 1

        time.sleep(t)

    def wait_for_element(self, lo: str = '', timeout: int = 10):
        """
        显式等待元素可见
        :param lo: 定位表达式（xpath/id）
        :param timeout: 超时时间（秒）
        :return: 元素可见返回True，否则抛TimeoutException
        """
        try:
            if lo.startswith('/'):
                locator = (By.XPATH, lo)
            else:
                locator = (By.ID, lo)
            # 等待元素可见
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            raise TimeoutException(f"元素 {lo} 在 {timeout} 秒内未可见")

    def enable_element(self, lo: str = ''):
        """
        启用禁用的元素（适配Test case 3：通过JS移除disabled属性）
        :param lo: 定位表达式
        """
        ele = self.__find_ele(lo)
        self.driver.execute_script("arguments[0].removeAttribute('disabled')", ele)


if __name__ == '__main__':
    a = Web()
    a.open_browser('gc')
    a.geturl("https://www.baidu.com/")
    a.assert_url("https://www.baidu.com/")
    a.assert_button("chat-submit-button")
    a.quit()
