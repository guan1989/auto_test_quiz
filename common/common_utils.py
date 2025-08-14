# -*- coding: utf-8 -*-
"""
@Time ： 2025/8/14 10:53
@Auth ： 张冠
@Function ：请输入模块功能描述
"""
from datetime import datetime
import os
from selenium.webdriver.remote.webdriver import WebDriver


class CommonUtils:
    def __init__(self, screenshot_dir="screenshots", report_dir="reports"):
        self.screenshot_dir = screenshot_dir  # 截图存放目录
        self.report_dir = report_dir  # 报告存放目录
        self.test_steps = []
        self._init_dirs()

    def _init_dirs(self):
        """初始化目录"""
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

    def take_screenshot(self, driver: WebDriver, step_desc: str) -> str:
        """截取截图并返回相对路径（相对于项目根目录）"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 替换特殊字符，避免路径错误
        filename = f"{step_desc}_{timestamp}.png".replace(" ", "_").replace("'", "")
        filepath = os.path.join(self.screenshot_dir, filename)
        driver.save_screenshot(filepath)
        print(f"截图保存成功：{filepath}")
        return filepath  # 返回相对路径（如：screenshots/xxx.png）

    def record_step(self, step_num: int, description: str, screenshot_path: str):
        self.test_steps.append({
            "step": step_num,
            "description": description,
            "screenshot": screenshot_path,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def generate_html_report(self, report_name=None):
        """生成HTML报告，使用相对路径引用截图"""
        if not report_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"test_report_{timestamp}.html"

        # 报告文件的完整路径（如：reports/test_report.html）
        report_path = os.path.join(self.report_dir, report_name)

        # 计算截图路径相对于报告文件的相对路径
        # 例如：报告在reports/，截图在screenshots/，则相对路径为"../screenshots/xxx.png"
        def get_relative_path(img_abs_path):
            # 获取报告文件所在目录的绝对路径
            report_dir_abs = os.path.abspath(self.report_dir)
            # 计算截图相对于报告目录的相对路径
            return os.path.relpath(img_abs_path, report_dir_abs)

        generate_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        html_content = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>登录测试报告</title>
            <style>
                body {{font-family: 'Microsoft YaHei', sans-serif; margin: 20px;}}
                .step {{margin: 15px 0; padding: 10px; border: 1px solid #eee; border-radius: 5px;}}
                .screenshot {{max-width: 800px; margin-top: 10px;}}
                .success {{color: #28a745;}}
                .failure {{color: #dc3545;}}
            </style>
        </head>
        <body>
            <h1>登录测试报告</h1>
            <p>生成时间: {generate_time}</p>
        """

        for step in self.test_steps:
            # 获取截图相对于报告的相对路径
            img_rel_path = get_relative_path(step["screenshot"])
            # 修复路径中的反斜杠为正斜杠（兼容浏览器）
            img_rel_path = img_rel_path.replace("\\", "/")

            html_content += f"""
            <div class="step">
                <h3>步骤 {step['step']}：{step['description']}</h3>
                <p>时间：{step['timestamp']}</p>
                <img src="{img_rel_path}" class="screenshot" 
                     alt="步骤 {step['step']} 的截图">
            </div>
            """

        html_content += """
            </body>
            </html>
        """

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"测试报告已生成：{os.path.abspath(report_path)}")
        return report_path
