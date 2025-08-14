# -*- coding: utf-8 -*-
"""
@Time ： 2025/8/14 11:43
@Auth ： 张冠
@Function ：请输入模块功能描述
"""
from selenium.webdriver.common.by import By


class LoginTestCase:
    def __init__(self, web, utils):
        self.web = web  # Web操作实例
        self.utils = utils  # 工具类实例
        self.base_url = "https://practicetestautomation.com/practice/"
        self.login_link_locator = (By.LINK_TEXT, "Test Login Page")

    def _open_login_page(self, step_counter):
        """打开登录页面（共用步骤）"""
        # 1. 打开主页面
        self.web.open_url(
            url=self.base_url,
            step_num=step_counter["num"],
            desc="打开测试网站主页"
        )
        step_counter["num"] += 1

        # 2. 点击登录链接
        self.web.click_element(
            by=self.login_link_locator[0],
            locator=self.login_link_locator[1],
            step_num=step_counter["num"],
            desc="点击'Test Login Page'链接，进入登录页面"
        )
        step_counter["num"] += 1
        return step_counter

    def test_positive_login(self):
        """测试用例1：正面登录测试（内部捕获异常，不中断后续用例）"""
        print("\n执行测试用例1：正面登录测试")
        step_counter = {"num": 1}  # 用字典便于修改内部值

        try:
            # 1. 打开登录页面
            step_counter = self._open_login_page(step_counter)

            # 2. 输入用户名
            self.web.input_text(
                by=By.ID,
                locator="username",
                text="student",
                step_num=step_counter["num"],
                desc="在用户名输入框中输入'student'"
            )
            step_counter["num"] += 1

            # 3. 输入密码
            self.web.input_text(
                by=By.ID,
                locator="password",
                text="Password123",
                step_num=step_counter["num"],
                desc="在密码输入框中输入'Password123'"
            )
            step_counter["num"] += 1

            # 4. 点击提交按钮
            self.web.click_element(
                by=By.ID,
                locator="submit",
                step_num=step_counter["num"],
                desc="点击登录提交按钮"
            )
            step_counter["num"] += 1

            # 5. 验证URL
            current_url = self.web.driver.current_url
            target_url = "practicetestautomation.com/logged-in-successfully/"
            assert target_url in current_url, \
                f"URL验证失败，当前URL: {current_url}"
            self.utils.record_step(
                step_num=step_counter["num"],
                description=f"验证新页面URL包含'{target_url}'，验证通过",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver,
                    f"验证URL_{step_counter['num']}"
                )
            )
            step_counter["num"] += 1

            # 6. 验证成功文本（修复：增加对"Logged In Successfully"的判断）
            success_text = self.web.get_element_text(by=By.TAG_NAME, locator="h1")
            expected_texts = ["Congratulations", "successfully logged in", "Logged In Successfully"]
            assert any(text in success_text for text in expected_texts), \
                f"成功文本验证失败，实际文本: {success_text}"
            self.utils.record_step(
                step_num=step_counter["num"],
                description=f"验证页面包含预期文本({expected_texts})，实际文本: {success_text}，验证通过",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver,
                    f"验证成功文本_{step_counter['num']}"
                )
            )
            step_counter["num"] += 1

            # 7. 验证登出按钮
            assert self.web.is_element_displayed(by=By.LINK_TEXT, locator="Log out"), \
                "登出按钮未显示"
            self.utils.record_step(
                step_num=step_counter["num"],
                description="验证登出按钮显示，验证通过",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver,
                    f"验证登出按钮_{step_counter['num']}"
                )
            )
            step_counter["num"] += 1

            print("测试用例1：执行成功")

        except AssertionError as ae:
            # 记录断言失败，但不中断程序
            self.utils.record_step(
                step_num=step_counter["num"],
                description=f"测试用例1失败：{str(ae)}",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver,
                    f"用例1失败_{step_counter['num']}"
                )
            )
            print(f"测试用例1：执行失败 - {str(ae)}")
        except Exception as e:
            self.utils.record_step(
                step_num=step_counter["num"],
                description=f"测试用例1发生错误：{str(e)}",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver,
                    f"用例1错误_{step_counter['num']}"
                )
            )
            print(f"测试用例1：发生错误 - {str(e)}")

    def test_negative_username(self):
        """测试用例2：负面用户名测试（内部捕获异常）"""
        print("\n执行测试用例2：负面用户名测试")
        step_counter = {"num": 1}

        try:
            # 1. 打开登录页面
            step_counter = self._open_login_page(step_counter)

            # 2. 输入错误用户名
            self.web.input_text(
                by=By.ID,
                locator="username",
                text="incorrectUser",
                step_num=step_counter["num"],
                desc="在用户名输入框中输入错误用户名'incorrectUser'"
            )
            step_counter["num"] += 1

            # 3. 输入正确密码
            self.web.input_text(
                by=By.ID,
                locator="password",
                text="Password123",
                step_num=step_counter["num"],
                desc="在密码输入框中输入正确密码'Password123'"
            )
            step_counter["num"] += 1

            # 4. 点击提交按钮
            self.web.click_element(
                by=By.ID,
                locator="submit",
                step_num=step_counter["num"],
                desc="点击登录提交按钮"
            )
            step_counter["num"] += 1

            # 5. 验证错误消息显示
            assert self.web.is_element_displayed(by=By.ID, locator="error"), \
                "错误消息未显示"
            self.utils.record_step(
                step_num=step_counter["num"],
                description="验证错误消息显示，验证通过",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver,
                    f"验证错误显示_{step_counter['num']}"
                )
            )
            step_counter["num"] += 1

            # 6. 验证错误消息文本
            error_text = self.web.get_element_text(by=By.ID, locator="error")
            expected_text = "Your username is invalid!"
            assert error_text == expected_text, \
                f"错误消息文本不正确，实际文本: {error_text}"
            self.utils.record_step(
                step_num=step_counter["num"],
                description=f"验证错误消息文本为'{expected_text}'，验证通过",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver,
                    f"验证错误文本_{step_counter['num']}"
                )
            )
            step_counter["num"] += 1

            print("测试用例2：执行成功")

        except AssertionError as ae:
            self.utils.record_step(
                step_num=step_counter["num"],
                description=f"测试用例2失败：{str(ae)}",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver,
                    f"用例2失败_{step_counter['num']}"
                )
            )
            print(f"测试用例2：执行失败 - {str(ae)}")
        except Exception as e:
            self.utils.record_step(
                step_num=step_counter["num"],
                description=f"测试用例2发生错误：{str(e)}",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver,
                    f"用例2错误_{step_counter['num']}"
                )
            )
            print(f"测试用例2：发生错误 - {str(e)}")

    def test_negative_password(self):
        """测试用例3：负面密码测试（内部捕获异常）"""
        print("\n执行测试用例3：负面密码测试")
        step_counter = {"num": 1}

        try:
            # 1. 打开登录页面
            step_counter = self._open_login_page(step_counter)

            # 2. 输入正确用户名
            self.web.input_text(
                by=By.ID,
                locator="username",
                text="student",
                step_num=step_counter["num"],
                desc="在用户名输入框中输入正确用户名'student'"
            )
            step_counter["num"] += 1

            # 3. 输入错误密码
            self.web.input_text(
                by=By.ID,
                locator="password",
                text="incorrectPassword",
                step_num=step_counter["num"],
                desc="在密码输入框中输入错误密码'incorrectPassword'"
            )
            step_counter["num"] += 1

            # 4. 点击提交按钮
            self.web.click_element(
                by=By.ID,
                locator="submit",
                step_num=step_counter["num"],
                desc="点击登录提交按钮"
            )
            step_counter["num"] += 1

            # 5. 验证错误消息显示
            assert self.web.is_element_displayed(by=By.ID, locator="error"), \
                "错误消息未显示"
            self.utils.record_step(
                step_num=step_counter["num"],
                description="验证错误消息显示，验证通过",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver,
                    f"验证错误显示_{step_counter['num']}"
                )
            )
            step_counter["num"] += 1

            # 6. 验证错误消息文本
            error_text = self.web.get_element_text(by=By.ID, locator="error")
            expected_text = "Your password is invalid!"
            assert error_text == expected_text, \
                f"错误消息文本不正确，实际文本: {error_text}"
            self.utils.record_step(
                step_num=step_counter["num"],
                description=f"验证错误消息文本为'{expected_text}'，验证通过",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver,
                    f"验证错误文本_{step_counter['num']}"
                )
            )
            step_counter["num"] += 1

            print("测试用例3：执行成功")

        except AssertionError as ae:
            self.utils.record_step(
                step_num=step_counter["num"],
                description=f"测试用例3失败：{str(ae)}",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver,
                    f"用例3失败_{step_counter['num']}"
                )
            )
            print(f"测试用例3：执行失败 - {str(ae)}")
        except Exception as e:
            self.utils.record_step(
                step_num=step_counter["num"],
                description=f"测试用例3发生错误：{str(e)}",
                screenshot_path=self.utils.take_screenshot(
                    self.web.driver,
                    f"用例3错误_{step_counter['num']}"
                )
            )
            print(f"测试用例3：发生错误 - {str(e)}")