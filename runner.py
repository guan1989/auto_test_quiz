# -*- coding: utf-8 -*-
"""
@Time ： 2025/8/14 23:15
@Auth ： 张冠
@Function ：请输入模块功能描述
"""
import os


from ddt.excel_ddt import ddt


# web用例
os.system('rd /s/q result/web')
os.system('rd /s/q report/web')
case_name = '测试用例.xlsx'
os.remove('./lib/cases/results/result-' + case_name)
ddt.run_web_cases(case_name)
os.system('allure generate ./result/web -o ./report/web --clean')

# # app用例
# os.system('rd /s/q result/app')
# os.system('rd /s/q report/app')
# case_name = 'APP自动化示例.xlsx'
# os.remove('./lib/cases/results/result-' + case_name)
# ddt.run_app_cases(case_name)
# os.system('allure generate ./result/app -o ./report/app --clean')
