# -*- coding: utf-8 -*-
"""
@Time ： 2025/8/14 23:15
@Auth ： 张冠
@Function ：请输入模块功能描述
"""
import os

from ddt.excel_ddt import ddt

os.system('rd /s/q result')
os.system('rd /s/q report')
case_name = '测试用例.xlsx'
os.remove('./lib/cases/results/result-' + case_name)
# ddt.run_web_cases("./lib/cases/" + case_name, "./lib/cases/results/result-" + case_name)
ddt.run_web_cases(case_name)
os.system('allure generate result -o report --clean')
