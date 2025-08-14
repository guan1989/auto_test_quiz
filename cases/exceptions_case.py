# -*- coding: utf-8 -*-
"""
@Time ： 2025/8/14 12:17
@Auth ： 张冠
@Function ：请输入模块功能描述
"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import (NoSuchElementException,
                                        ElementNotInteractableException,
                                        InvalidElementStateException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ExceptionsTestCase:
    def __init__(self, web, utils):
        self.web = web  # Web操作实例
        self.utils = utils  # 工具类实例
        self.base_url = "https://practicetestautomation.com/practice-test-exceptions/"
        self.step_counter = 1  # 步骤计数器

    def _reset_step_counter(self):
        """重置步骤计数器"""
        self.step_counter = 1

    def _get_current_step(self):
        """获取当前步骤号并自增"""
        current = self.step_counter
        self.step_counter += 1
        return current

    def test_no_such_element_exception(self):
        """测试用例1：验证NoSuchElementException（无等待情况下）"""
        print("\n执行测试用例1：NoSuchElementException测试")
        self._reset_step_counter()

        try:
            # 1. 打开页面
            self.web.open_url(
                url=self.base_url,
                step_num=self._get_current_step(),
                desc="打开Test Exceptions页面"
            )

            # 2. 点击Add按钮
            self.web.click_element(
                by=By.ID,
                locator="add_btn",
                step_num=self._get_current_step(),
                desc="点击Add按钮"
            )

            # 3. 不等待直接查找第二行输入框（预期会抛出NoSuchElementException）
            step = self._get_current_step()
            try:
                # 故意不添加等待，直接查找元素
                self.web.driver.find_element(By.ID, "row2_input")
                # 如果找到元素，记录异常
                self.utils.record_step(
                    step_num=step,
                    description="测试用例1失败：未抛出NoSuchElementException，找到了元素",
                    screenshot_path=self.utils.take_screenshot(
                        self.web.driver, f"用例1_未抛出异常_{step}"
                    )
                )
                print("测试用例1失败：未抛出预期的NoSuchElementException")
            except NoSuchElementException:
                # 捕获到预期异常，记录成功
                self.utils.record_step(
                    step_num=step,
                    description="测试用例1成功：捕获到预期的NoSuchElementException",
                    screenshot_path=self.utils.take_screenshot(
                        self.web.driver, f"用例1_捕获异常_{step}"
                    )
                )
                print("测试用例1成功：捕获到预期的NoSuchElementException")

        except Exception as e:
            self.utils.record_step(
                step_num=self._get_current_step(),
                description=f"测试用例1发生意外错误：{str(e)}",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver, f"用例1_意外错误"
                )
            )
            print(f"测试用例1发生意外错误：{str(e)}")

    def test_element_not_interactable_exception(self):
        """测试用例2：验证ElementNotInteractableException"""
        print("\n执行测试用例2：ElementNotInteractableException测试")
        self._reset_step_counter()

        try:
            # 1. 打开页面
            self.web.open_url(
                url=self.base_url,
                step_num=self._get_current_step(),
                desc="打开Test Exceptions页面"
            )

            # 2. 点击Add按钮
            self.web.click_element(
                by=By.ID,
                locator="add_btn",
                step_num=self._get_current_step(),
                desc="点击Add按钮"
            )

            # 3. 等待第二行加载（10秒超时）
            step = self._get_current_step()
            row2_xpath = "//*[@id='row2']/input"

            WebDriverWait(self.web.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, row2_xpath))
            )
            self.utils.record_step(
                step_num=step,
                description="第二行输入框已显示",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver, f"用例2_第二行显示_{step}"
                )
            )

            # 4. 在第二行输入框中输入文本
            step = self._get_current_step()
            self.web.input_text(
                by=By.XPATH,
                locator="/*[@id='row2']/input",
                text="测试文本",
                step_num=step,
                desc="在第二行输入框中输入文本"
            )

            # 5. 尝试点击name="Save"的不可见元素（预期抛出异常）
            step = self._get_current_step()
            try:
                # 定位到第一个不可见的Save按钮
                save_buttons = self.web.driver.find_elements(By.NAME, "Save")
                invisible_button = save_buttons[0]  # 第一个是不可见的
                invisible_button.click()

                # 如果未抛出异常，记录失败
                self.utils.record_step(
                    step_num=step,
                    description="测试用例2失败：未抛出ElementNotInteractableException",
                    screenshot_path=self.utils.take_screenshot(
                        self.web.driver, f"用例2_未抛出异常_{step}"
                    )
                )
                print("测试用例2失败：未抛出预期的ElementNotInteractableException")

            except ElementNotInteractableException:
                # 捕获到预期异常，记录成功
                self.utils.record_step(
                    step_num=step,
                    description="测试用例2成功：捕获到预期的ElementNotInteractableException",
                    screenshot_path=self.utils.take_screenshot(
                        self.web.driver, f"用例2_捕获异常_{step}"
                    )
                )
                print("测试用例2成功：捕获到预期的ElementNotInteractableException")

                # 点击可见的Save按钮完成操作
                visible_button = save_buttons[1]
                visible_button.click()

                # 验证文本已保存
                step = self._get_current_step()
                saved_text = self.web.get_element_text(by=By.ID, locator="confirmation")
                assert "Row 2 saved" in saved_text, f"保存验证失败，实际文本: {saved_text}"
                self.utils.record_step(
                    step_num=step,
                    description=f"验证文本已保存，实际文本: {saved_text}",
                    screenshot_path=self.utils.take_screenshot(
                        self.web.driver, f"用例2_验证保存_{step}"
                    )
                )

        except Exception as e:
            self.utils.record_step(
                step_num=self._get_current_step(),
                description=f"测试用例2发生意外错误：{str(e)}",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver, f"用例2_意外错误"
                )
            )
            print(f"测试用例2发生意外错误：{str(e)}")

    def test_invalid_element_state_exception(self):
        """测试用例3：验证InvalidElementStateException"""
        print("\n执行测试用例3：InvalidElementStateException测试")
        self._reset_step_counter()

        try:
            # 1. 打开页面
            self.web.open_url(
                url=self.base_url,
                step_num=self._get_current_step(),
                desc="打开Test Exceptions页面"
            )

            # 2. 尝试清除禁用的输入框（预期抛出异常）
            step = self._get_current_step()
            try:
                disabled_field = self.web.driver.find_element(By.ID, "input1")
                disabled_field.clear()  # 尝试清除禁用字段

                # 如果未抛出异常，记录失败
                self.utils.record_step(
                    step_num=step,
                    description="测试用例3失败：未抛出InvalidElementStateException",
                    screenshot_path=self.utils.take_screenshot(
                        self.web.driver, f"用例3_未抛出异常_{step}"
                    )
                )
                print("测试用例3失败：未抛出预期的InvalidElementStateException")

            except (InvalidElementStateException, ElementNotInteractableException):
                # 捕获到预期异常，记录成功
                self.utils.record_step(
                    step_num=step,
                    description="测试用例3成功：捕获到预期的异常（禁用元素操作）",
                    screenshot_path=self.utils.take_screenshot(
                        self.web.driver, f"用例3_捕获异常_{step}"
                    )
                )
                print("测试用例3成功：捕获到预期的异常（禁用元素操作）")

                # 点击Edit按钮启用输入框
                step = self._get_current_step()
                self.web.click_element(
                    by=By.ID,
                    locator="edit_btn",
                    step_num=step,
                    desc="点击Edit按钮启用输入框"
                )

                # 清除并输入文本
                step = self._get_current_step()
                self.web.input_text(
                    by=By.ID,
                    locator="input1",
                    text="修改后的文本",
                    step_num=step,
                    desc="在启用的输入框中输入新文本"
                )

                # 点击Save按钮
                step = self._get_current_step()
                self.web.click_element(
                    by=By.ID,
                    locator="save_btn",
                    step_num=step,
                    desc="点击Save按钮保存修改"
                )

                # 验证文本已修改
                step = self._get_current_step()
                saved_text = self.web.get_element_text(by=By.ID, locator="confirmation")
                assert "Input 1 saved" in saved_text, f"修改验证失败，实际文本: {saved_text}"
                self.utils.record_step(
                    step_num=step,
                    description=f"验证文本已修改，实际文本: {saved_text}",
                    screenshot_path=self.utils.take_screenshot(
                        self.web.driver, f"用例3_验证修改_{step}"
                    )
                )

        except Exception as e:
            self.utils.record_step(
                step_num=self._get_current_step(),
                description=f"测试用例3发生意外错误：{str(e)}",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver, f"用例3_意外错误"
                )
            )
            print(f"测试用例3发生意外错误：{str(e)}")

    def test_stale_element_reference_exception(self):
        """测试用例4：验证StaleElementReferenceException"""
        print("\n执行测试用例4：StaleElementReferenceException测试")
        self._reset_step_counter()

        try:
            # 1. 打开页面
            self.web.open_url(
                url=self.base_url,
                step_num=self._get_current_step(),
                desc="打开Test Exceptions页面"
            )

            # 2. 获取指令文本元素
            step = self._get_current_step()
            instructions = self.web.driver.find_element(By.ID, "instructions")
            self.utils.record_step(
                step_num=step,
                description="获取指令文本元素的引用",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver, f"用例4_获取元素_{step}"
                )
            )

            # 3. 点击Add按钮（会导致指令元素被移除）
            step = self._get_current_step()
            self.web.click_element(
                by=By.ID,
                locator="add_btn",
                step_num=step,
                desc="点击Add按钮（移除指令元素）"
            )

            # 4. 尝试访问已失效的元素引用（预期抛出异常）
            step = self._get_current_step()
            try:
                # 尝试访问已被移除的元素
                instructions.text
                # 如果未抛出异常，记录失败
                self.utils.record_step(
                    step_num=step,
                    description="测试用例4失败：未抛出StaleElementReferenceException",
                    screenshot_path=self.utils.take_screenshot(
                        self.web.driver, f"用例4_未抛出异常_{step}"
                    )
                )
                print("测试用例4失败：未抛出预期的StaleElementReferenceException")

            except StaleElementReferenceException:
                # 捕获到预期异常，记录成功
                self.utils.record_step(
                    step_num=step,
                    description="测试用例4成功：捕获到预期的StaleElementReferenceException",
                    screenshot_path=self.utils.take_screenshot(
                        self.web.driver, f"用例4_捕获异常_{step}"
                    )
                )
                print("测试用例4成功：捕获到预期的StaleElementReferenceException")

        except Exception as e:
            self.utils.record_step(
                step_num=self._get_current_step(),
                description=f"测试用例4发生意外错误：{str(e)}",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver, f"用例4_意外错误"
                )
            )
            print(f"测试用例4发生意外错误：{str(e)}")

    def test_timeout_exception(self):
        """测试用例5：验证TimeoutException"""
        print("\n执行测试用例5：TimeoutException测试")
        self._reset_step_counter()

        try:
            # 1. 打开页面
            self.web.open_url(
                url=self.base_url,
                step_num=self._get_current_step(),
                desc="打开Test Exceptions页面"
            )

            # 2. 点击Add按钮
            step = self._get_current_step()
            self.web.click_element(
                by=By.ID,
                locator="add_btn",
                step_num=step,
                desc="点击Add按钮"
            )

            # 3. 等待3秒（元素5秒后出现，预期超时）
            step = self._get_current_step()
            try:
                # 设置3秒超时，预期会超时
                WebDriverWait(self.web.driver, 3).until(
                    EC.visibility_of_element_located((By.ID, "row2_input"))
                )

                # 如果未超时，记录失败
                self.utils.record_step(
                    step_num=step,
                    description="测试用例5失败：未抛出TimeoutException",
                    screenshot_path=self.utils.take_screenshot(
                        self.web.driver, f"用例5_未抛出异常_{step}"
                    )
                )
                print("测试用例5失败：未抛出预期的TimeoutException")

            except TimeoutException:
                # 捕获到预期异常，记录成功
                self.utils.record_step(
                    step_num=step,
                    description="测试用例5成功：捕获到预期的TimeoutException",
                    screenshot_path=self.utils.take_screenshot(
                        self.web.driver, f"用例5_捕获异常_{step}"
                    )
                )
                print("测试用例5成功：捕获到预期的TimeoutException")

                # 额外等待确保元素出现，不影响测试结果
                WebDriverWait(self.web.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "row2_input"))
                )

        except Exception as e:
            self.utils.record_step(
                step_num=self._get_current_step(),
                description=f"测试用例5发生意外错误：{str(e)}",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver, f"用例5_意外错误"
                )
            )
            print(f"测试用例5发生意外错误：{str(e)}")

    def run_all_exceptions_tests(self):
        """运行所有异常测试用例"""
        # self.test_no_such_element_exception()
        self.test_element_not_interactable_exception()
        # self.test_invalid_element_state_exception()
        # self.test_stale_element_reference_exception()
        # self.test_timeout_exception()