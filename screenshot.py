#!/usr/bin/env python3

# 截图

import subprocess
import sys
from datetime import datetime
import os
import argparse
from PIL import Image # pip install pillow
import io

def capture_screenshot(filename_prefix=None, scale=1.0):
    # 构建文件名
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # 当未提供前缀时，只使用时间戳作为文件名
    filename = f"{filename_prefix}-{timestamp}.png" if filename_prefix else f"{timestamp}.png"
    filepath = os.path.expanduser(f"~/Desktop/{filename}")

    # 执行 adb 命令并捕获输出
    process = subprocess.Popen("adb exec-out screencap -p", shell=True, stdout=subprocess.PIPE)
    output, _ = process.communicate()

    # 使用 PIL 来缩放图片
    image = Image.open(io.BytesIO(output))
    new_size = (int(image.width * scale), int(image.height * scale))
    resized_image = image.resize(new_size, Image.ADAPTIVE)

    # 保存缩放后的图片
    with open(filepath, 'wb') as file:
        resized_image.save(file, "PNG")

    print(f"Screenshot saved as {filepath}")

if __name__ == "__main__":
    # 创建解析器
    parser = argparse.ArgumentParser(description='Capture a screenshot.')
    parser.add_argument('-name', type=str, help='the prefix of the filename')
    parser.add_argument('-scale', type=float, help='scale of the screenshot', default=1.0)

    # 解析参数
    args = parser.parse_args()

    # 使用参数
    filename_prefix = args.name
    scale = args.scale

    capture_screenshot(filename_prefix, scale)
