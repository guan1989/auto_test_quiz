# -*- coding: utf-8 -*-
"""
@Time ： 2025/8/16 20:19
@Auth ： 张冠
@Function ：请输入模块功能描述
"""
import json
import os
import threading
import time
from appium import webdriver

from common.Logger import logger
from appium.options.android import UiAutomator2Options


class App:

    def __init__(self):
        # 定义driver对象，指定类型
        self.driver: webdriver.Remote = None
        self.port = '4723'

    def stop_appium(self, port=''):
        """
        停止appium
        :param port: 通过端口去杀进程
        """
        # 关闭和启动使用通用的port
        if not port:
            port = self.port

        res = os.popen(f'netstat -aon | findstr {port}').read().split('\n')
        logger.debug(res)
        if res:
            res = res[0]
        else:
            logger.warning('没有找到appium进程')
            return

        res = res.split(' ')
        logger.debug(res)
        # 找到了进程
        if len(res) > 1:
            pid = res[-1]
            os.system(f'taskkill /F /pid {pid}')
            logger.info('已经结束appium进程')
        else:
            logger.warning('没有找到appium进程')

    def run_appium(self, port='4723'):
        """
        启动appium服务
        :param port: 启动端口
        :return:
        """

        self.stop_appium(port)
        self.port = port

        def __run_appium():
            os.system(
                r'node "D:\Program Files\Appium\resources\app\node_modules\appium\build\lib\main.js" '
                rf'--port {port} --chromedriver-executable dd')
            # 用多线程启动

        th = threading.Thread(target=__run_appium)
        th.start()
        logger.info('appium服务正在启动...')
        time.sleep(5)



    def run_app(self, conf: str = ''):
        """
        app启动的标准配置，需要传递json字符串
        :param conf: json字符串配置
        """
        conf_dict  = json.loads(conf)

        # 主动连接设备
        os.system('adb devices')

        options = UiAutomator2Options()
        options.device_name = conf_dict.get("deviceName")
        options.udid = conf_dict.get("deviceName")
        options.app_package = conf_dict.get("appPackage")
        options.app_activity = conf_dict.get("appActivity")
        options.automation_name = "UiAutomator2"

        self.driver = webdriver.Remote(
            f"http://127.0.0.1:{self.port}/wd/hub",
            options=options
        )
        self.driver.implicitly_wait(5)

    def __find_ele(self, lo: str = ''):
        """
        统一定位元素
        :param lo: 支持accessibility id, id , xpath
        """
        if lo.startswith('/') or lo.startswith('('):
            # 这是xpath
            ele = self.driver.find_element('xpath', lo)
        elif lo.__contains__(':id/'):
            # 这是id
            ele = self.driver.find_element('id', lo)
        else:
            # 其他情况，我们认为都是通过描述文字定位
            ele = self.driver.find_element('accessibility id', lo)

        return ele

    def click(self, lo: str = ''):
        """点击元素"""
        ele = self.__find_ele(lo)
        ele.click()

    def input(self, lo: str = '', text: str = '', is_clear: str = ''):
        """
        输入文本
        :param lo: 定位
        :param text: 需要输入的字符串
        :param is_clear: 输入任意字符都代表先清空再输入
        :return:
        """
        ele = self.__find_ele(lo)
        if is_clear:
            ele.clear()
            ele.send_keys(text)
        else:
            ele.send_keys(text)

    def keyevent(self, keycode='66'):
        """
        按键
        :param keycode: 默认66，回车
        """
        try:
            keycode = int(keycode)
        except:
            keycode = 66

        self.driver.keyevent(keycode)

    def sleep(self, t='1'):
        try:
            t = int(t)
        except:
            t = 1

        time.sleep(t)

    def quit(self):
        """退出APP"""
        time.sleep(2)
        self.driver.quit()
        self.driver = None

    def assert_text(self, xpath: str, expected_text: str):
        """
        断言页面元素的文本内容是否符合预期
        :param xpath: xpath定位表达式
        :param expected_text: 预期的文本结果
        :raises AssertionError: 当实际文本与预期文本不一致时抛出断言错误
        """
        try:
            # 通过xpath定位元素
            ele = self.driver.find_element('xpath', xpath)
            # 获取元素实际文本
            actual_text = ele.text
            # 断言实际文本与预期文本一致
            assert actual_text == expected_text, \
                f"文本断言失败！预期: {expected_text}, 实际: {actual_text}"
            logger.info(f"文本断言成功！预期: {expected_text}, 实际: {actual_text}")
        except Exception as e:
            logger.error(f"文本断言出错: {str(e)}")
            raise  # 重新抛出异常，确保断言失败被捕获
