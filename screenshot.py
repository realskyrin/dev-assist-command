#!/usr/bin/env python3

# 截图

import subprocess
import sys
from datetime import datetime
import os

def capture_screenshot(filename_prefix=None):
    # 构建文件名
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # 当未提供前缀时，只使用时间戳作为文件名
    filename = f"{filename_prefix}-{timestamp}.png" if filename_prefix else f"{timestamp}.png"
    filepath = os.path.expanduser(f"~/Desktop/{filename}")

    # 执行 adb 命令并捕获输出
    process = subprocess.Popen("adb exec-out screencap -p", shell=True, stdout=subprocess.PIPE)
    output, _ = process.communicate()

    # 直接保存输出到文件
    with open(filepath, 'wb') as file:
        file.write(output)

    print(f"Screenshot saved as {filepath}")

if __name__ == "__main__":
    # 检查是否有提供参数
    filename_prefix = sys.argv[1] if len(sys.argv) > 1 else None
    capture_screenshot(filename_prefix)
