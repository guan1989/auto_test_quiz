# -*- coding: utf-8 -*-
"""
@Time ： 2025/8/14 22:44
@Auth ： 张冠
@Function ：请输入模块功能描述
"""
import logging
import os

import yaml

# 项目名字
proname = 'auto_test_quiz'
# 获取项目绝对路径
path = os.path.abspath(__file__)
# 明确入口的名字进行截取
path = path[:path.find(proname)] + proname + '\\'
print(path)

# 读取日志的配置
with open(file=path + "lib/conf.yml", mode='r', encoding="utf-8") as file:
    logging_yaml = yaml.safe_load(stream=file).get('logger')
    logging_yaml['filename'] = path + logging_yaml.get('filename')

fh = logging.FileHandler(logging_yaml.get('filename'), encoding='utf-8', mode=logging_yaml.get('filemode'))
fh.setFormatter(logging.Formatter(logging_yaml['format']))
# 获取根记录器：配置信息从yaml文件中获取
logger = logging.getLogger()
logger.setLevel(logging_yaml['level'])
logger.addHandler(fh)

# 创建输出到控制台的输出流
console = logging.StreamHandler()
# 设置日志等级
console.setLevel(logging_yaml['level'])
# 设置日志格式
console.setFormatter(logging.Formatter(logging_yaml['format']))
# 添加到logger输出
logger.addHandler(console)



if __name__ == "__main__":
    # 等级顺序
    logger.debug("DEBUG")
    logger.info("INFO")
    logger.warning('WARNING')
    logger.error('ERROR')