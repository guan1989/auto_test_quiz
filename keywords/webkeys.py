# -*- coding: utf-8 -*-
"""
@Time ： 2025/8/14 20:50
@Auth ： 张冠
@Function ：请输入模块功能描述
"""
import os

from selenium import webdriver
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
        if lo.startswith('/'):
            ele = self.driver.find_element('xpath', lo)
        elif lo.startswith('$'):
            name_value = lo[1:]  # 去掉前缀$
            ele = self.driver.find_element('name', name_value)
        elif lo.startswith('link_test'):
            name_value = lo[8:]  # 去掉前缀
            # ele = self.driver.find_element('LINK_TEXT', name_value)
            ele=self.driver.find_element(By.LINK_TEXT,name_value)
        else:
            ele = self.driver.find_element('id', lo)
        # 操作元素高亮
        if ele:
            self.driver.execute_script("arguments[0].style.background = '#4aff00'", ele)

        return ele

    def input(self, lo: str = '', value: str = "", ):
        """
        往元素里面输入
        :param value: 要输入的值
        :param lo: 定位表达式，支持xpath，id
        :return:
        """
        ele = self.__find_ele(lo)
        ele.send_keys(value)

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
        ele = self.__find_ele(lo)
        ele.click()

    def quit(self):
        """关闭浏览器"""
        self.driver.quit()
        self.driver = None

    def assert_text(self, lo: str = '', expected_text: str = '', timeout: int = 10):
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
            # 等待元素可见
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(loc)
            )
            actual_text = element.text.strip()
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
        try:
            # 获取定位器元组
            loc = self.__find_ele(lo)
            # 等待元素可见
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(loc)
            )
            # 额外检查确保元素确实可见（双重保障）
            assert element.is_displayed(), f"按钮 '{lo}' 存在但不可见"
            # 校验按键文本
            actual_text = element.text.strip()
            if expected_text == actual_text:
                return True
            else:
                raise AssertionError(f"按键存但与预期值不符。预期值: {expected_text},实际值：{actual_text}")


        except Exception as e:
            raise AssertionError(f"验证按钮失败: {str(e)}")


if __name__ == '__main__':
    a = Web()
    a.open_browser('gc')
    a.geturl("https://www.baidu.com/")
    a.assert_url("https://www.baidu.com/")
    a.assert_button("chat-submit-button")
    a.quit()
