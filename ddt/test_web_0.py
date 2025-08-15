# -*- coding: utf-8 -*-
"""
@Time ： 2025/8/14 23:00
@Auth ： 张冠
@Function ：请输入模块功能描述
"""
import allure
import pytest
from common.Logger import logger
from ddt.excel_ddt import ddt


@allure.feature(f'#{ddt.f_idx} {ddt.feature}')
class Test_Web:
    """通用测试类，可以执行任意一个testsuite"""

    @allure.step
    def run_step(self, args):
        """反射执行"""
        # 先截图再退出浏览器
        # if args[0] == 'quit':
        #     allure.attach(ddt.obj.driver.get_screenshot_as_png(), '成功截图', allure.attachment_type.PNG)
        # 反射获取函数
        func = getattr(ddt.obj, args[0])
        # 执行函数，并返回结果


        if ddt.obj.driver:  # 确保浏览器实例存在
            allure.attach(
                ddt.obj.driver.get_screenshot_as_png(),
                f"步骤[{args[0]}]截图",  # 截图描述（可关联步骤名）
                allure.attachment_type.PNG
            )
        return func(*args[1:])

    @allure.story(f'#{ddt.s_idx} {ddt.story}')
    @pytest.mark.parametrize('case', ddt.testsuite)
    def test_suite(self, case):
        """
        测试用例集，执行函数
        每次参数化执行一条用例
        :param case: 整条用例的步骤
        """
        # print(case)
        # 所以步骤的第一行的第二个单元格就是title
        allure.dynamic.title(case[0][1])
        # 因为不执行，所以也不写入
        ddt.writer.row += 1

        # 剩下的都是步骤，都是需要执行的
        case = case[1:]

        # 记录跑了多少行
        run_rows = 0

        try:
            # 使用try执行用例，一旦用例执行报错，就停止，并开始截图
            for c in case:
                # 每跑一行run_rows + 1
                run_rows += 1

                # 先获取参数，再反射执行
                # 获取参数，是一行里面4~6这三个元素
                params = c[3:7]
                # 对参数从右往左找，找最后一个不为空的，然后把所有空的全部截掉
                # 兼容都是空的情况
                index = -1
                for i in range(3, -1, -1):
                    if len(params[i]) > 0:
                        index = i
                        break

                params = params[0:index + 1]

                # 这里反射执行
                with allure.step(c[2]):
                    # 记录关键字执行的结果
                    res = self.run_step(params)

                # 如果能执行到这里，就说明关键字执行是成功的
                ddt.writer.write(ddt.writer.row, 7, 'PASS', 3)
                ddt.writer.write(ddt.writer.row, 8, str(res))
                ddt.writer.row += 1

            # 要求每一步操作均有截图，在run_step做了处理，此处不在重复截图
            # if ddt.obj.driver:
            #     allure.attach(ddt.obj.driver.get_screenshot_as_png(), '成功截图', allure.attachment_type.PNG)
        except Exception as e:
            msg = e.__str__()
            msg = msg[:msg.find('Stacktrace')]

            # 如果执行失败，就写入失败的结果
            ddt.writer.write(ddt.writer.row, 7, 'FAIL', 2)
            ddt.writer.write(ddt.writer.row, 8, msg)
            # ddt.writer.write(ddt.writer.row, 8, traceback.format_exc())
            # 剩下的步骤，在写入结果的时候需要跳过
            ddt.writer.row += len(case) + 1 - run_rows

            logger.exception(e)
            if ddt.obj.driver:
                allure.attach(ddt.obj.driver.get_screenshot_as_png(), '失败', allure.attachment_type.PNG)
            # 让用例主动失败
            pytest.fail(msg)