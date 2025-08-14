# -*- coding: utf-8 -*-
"""
@Time ： 2025/8/14 10:34
@Auth ： 张冠
@Function ：请输入模块功能描述
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time


class Web:
    def __init__(self, driver: WebDriver, utils, implicit_wait=10):
        self.driver = driver
        self.utils = utils  # 公共工具类实例
        self.driver.implicitly_wait(implicit_wait)  # 设置隐式等待

    def open_url(self, url: str, step_num: int, desc: str = "打开URL") -> bool:
        """打开指定URL"""
        try:
            self.driver.get(url)
            self.driver.maximize_window()
            time.sleep(2)  # 等待页面加载
            screenshot = self.utils.take_screenshot(self.driver, f"打开URL_{url}")
            self.utils.record_step(step_num, desc, screenshot)
            return True
        except Exception as e:
            screenshot = self.utils.take_screenshot(self.driver, f"打开URL失败_{url}")
            self.utils.record_step(step_num, f"{desc}失败：{str(e)}", screenshot)
            return False

    def click_element(self, by=By.ID, locator: str = None, step_num: int = None,
                      desc: str = "点击元素") -> bool:
        """点击指定元素"""
        try:
            element = self.driver.find_element(by, locator)
            element.click()
            time.sleep(1.5)  # 等待交互完成
            screenshot = self.utils.take_screenshot(self.driver, f"点击_{locator}")
            self.utils.record_step(step_num, desc, screenshot)
            return True
        except (NoSuchElementException, TimeoutException) as e:
            screenshot = self.utils.take_screenshot(self.driver, f"点击失败_{locator}")
            self.utils.record_step(step_num, f"{desc}失败（{locator}）：{str(e)}", screenshot)
            return False

    def input_text(self, by=By.ID, locator: str = None, text: str = "",
                   step_num: int = None, desc: str = "输入文本") -> bool:
        """向指定元素输入文本"""
        try:
            element = self.driver.find_element(by, locator)
            element.clear()  # 清空输入框
            element.send_keys(text)
            screenshot = self.utils.take_screenshot(self.driver, f"输入_{locator}")
            self.utils.record_step(step_num, desc, screenshot)
            return True
        except (NoSuchElementException, TimeoutException) as e:
            screenshot = self.utils.take_screenshot(self.driver, f"输入失败_{locator}")
            self.utils.record_step(step_num, f"{desc}失败（{locator}）：{str(e)}", screenshot)
            return False

    def go_back(self, step_num: int, desc: str = "返回上一页") -> bool:
        """返回上一页"""
        try:
            self.driver.back()
            time.sleep(2)
            screenshot = self.utils.take_screenshot(self.driver, "返回上一页")
            self.utils.record_step(step_num, desc, screenshot)
            return True
        except Exception as e:
            screenshot = self.utils.take_screenshot(self.driver, "返回失败")
            self.utils.record_step(step_num, f"{desc}失败：{str(e)}", screenshot)
            return False

    def get_element_text(self, by=By.ID, locator: str = None) -> str:
        """获取元素文本"""
        try:
            element = self.driver.find_element(by, locator)
            return element.text
        except NoSuchElementException:
            print(f"未找到元素: {locator}")
            return None

    def is_element_displayed(self, by=By.ID, locator: str = None) -> bool:
        """检查元素是否显示"""
        try:
            element = self.driver.find_element(by, locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False
