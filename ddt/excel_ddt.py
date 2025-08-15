# -*- coding: utf-8 -*-
"""
@Time ： 2025/8/14 22:55
@Auth ： 张冠
@Function ：请输入模块功能描述
"""
import datetime
import os
import pytest

from keywords.webkeys import Web
from common.Excel import Reader, Writer
from common.Logger import logger, path


class DDT:
    """数据驱动类"""

    def __init__(self):
        # 先创建关键字对象
        self.obj: Web = None
        self.reader = Reader()
        self.writer = Writer()

        # 存储一个用例集的用例，一个测试用例步骤
        self.testsuite = []
        self.testcase = []

        # 使用suite_idx，记录执行的test_suite序号
        self.suite_idx = 0

        # 分组定制
        self.story = ''
        self.s_idx = 0

        self.feature = ''
        self.f_idx = 0

        # 自动化类型
        self.type = 'web'

    def __run_test(self):
        # 每一个test_suite执行前，都把上一次执行的test_web_x.py重命名为
        # test_web_x+1.py，然后再去执行

        os.rename(path + f'ddt\\test_{self.type}_{self.suite_idx}.py',
                  path + f'ddt\\test_{self.type}_{self.suite_idx + 1}.py')
        pytest.main(['-s', path + f'ddt\\test_{self.type}_{self.suite_idx + 1}.py', '--alluredir', './result'])
        # 跑完后，suite_idx + 1
        self.suite_idx += 1

    def run_web_cases(self, case_path='测试用例.xlsx'):
        """
        读取用例为三维列表，并执行
        :param case_path: 用例路径
        """
        self.obj = Web()
        self.type = 'web'

        # 打开一个excel
        self.reader.open_excel(path + 'lib/cases/' + case_path)
        # 复制新建一个结果文件写入
        self.writer.copy_open(path + 'lib/cases/' + case_path, path + 'lib/cases/results/result-' + case_path)

        # 获取所有sheet
        sheets = self.reader.get_sheets()

        # 存储一个用例集的用例，一个测试用例步骤
        self.testsuite = []
        self.testcase = []

        # 记录开始时间，并写入到第一个sheet的第二行，第三列
        start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.writer.set_sheet(sheets[0])
        self.writer.write(1, 3, start_time)

        for sheet in sheets:
            # 设置读取的sheet页面
            self.reader.set_sheet(sheet)
            self.writer.set_sheet(sheet)

            # feature其实就是sheet名字，切换的时候记录
            self.feature = sheet
            self.f_idx += 1
            # 一个sheet的testsuite的序号独立统计
            self.s_idx = 0

            # 读取当前sheet的所有行
            lines = self.reader.readline()
            logger.debug(lines)
            # 遍历每一行，然后执行
            for i in range(1, len(lines)):
                line = lines[i]

                if len(line[0]) > 0:
                    # 说明读到了一个testsuite
                    if self.testcase:
                        # 如果前面在统计一组testsuite，到下一组testsuite的时候
                        # 说明这组testsuite统计完了，我们把最后一个测试用例添加到testsuite里面
                        self.testsuite.append(self.testcase)

                    # 这里执行该组testsuite
                    if self.testsuite:
                        # 有统计到用例才执行
                        self.__run_test()

                    # 统计到story名字
                    self.story = line[0]
                    self.s_idx += 1

                    # 记录testsuite开始写入的行数
                    # 因为分组本身不用执行，i+1
                    self.writer.row = i + 1

                    # 然后再统计下一组testsuite和testcase
                    self.testsuite = []
                    self.testcase = []
                elif len(line[1]) > 0:
                    # 说明读到了一个testcase
                    if self.testcase:
                        # 如果前面在统计一组用例，到下一组用例的时候
                        # 说明这组用例统计完了，需要加到testsuite里面
                        self.testsuite.append(self.testcase)

                    # 然后再统计下一组用例
                    self.testcase = []
                    # 再把用例标题这一行放到用例最开始
                    self.testcase.append(line)
                else:
                    # 说明是测试步骤teststep
                    # 测试步骤直接放到测试用例的列表里面
                    self.testcase.append(line)

            # 当一个sheet遍历完，我们需要把最后一组testsuite做统计
            if self.testcase:
                # 如果前面在统计一组testsuite，到下一组testsuite的时候
                # 说明这组testsuite统计完了，我们把最后一个测试用例添加到testsuite里面
                self.testsuite.append(self.testcase)

            # 这里执行该组testsuite
            if self.testsuite:
                # 有统计到用例才执行
                self.__run_test()

            # 然后再统计下一个sheet的testsuite和testcase
            self.testsuite = []
            self.testcase = []

        # 记录结束时间，并写入到第一个sheet的第二行，第四列
        start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.writer.set_sheet(sheets[0])
        self.writer.write(1, 4, start_time)

        # 把文件名改回去
        self.writer.save_close()
        os.rename(path + f'ddt\\test_{self.type}_{self.suite_idx}.py', 'ddt\\test_web_0.py')


ddt = DDT()
