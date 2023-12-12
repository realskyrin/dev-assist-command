#!/usr/bin/env python3

# 截图

import subprocess
from datetime import datetime
import os
import argparse
from PIL import Image, UnidentifiedImageError # pip install pillow
import io
import time
import tempfile
from threading import Thread, Event

class TermLoading():
    def __init__(self):
        self.__threadEvent = Event()
        self.__thread = Thread(target=self.__loading, daemon=True)

    def show_loading(self):
        self.__threadEvent.clear()
        if not self.__thread.is_alive():
            self.__thread.start()

    def stop_loading(self):
        self.__threadEvent.set()

    def __loading(self):
        emojis = ["🌕", "🌖", "🌗", "🌘", "🌑", "🌒", "🌓", "🌔"]
        # emojis = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
        # emojis = ["🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚"]
        i = 0
        while True:
            while not self.__threadEvent.is_set():
                i = (i + 1) % len(emojis)
                print('\r' + emojis[i], end='', flush=True)
                time.sleep(0.1)
            print('\r', end='', flush=True)  # clear the line
            self.__threadEvent.wait()
            self.__threadEvent.clear()

def capture_screenshot(filename_prefix=None, scale=1.0, copy_to_clipboard=False, output_dir="~/Desktop"):
    # 构建文件名
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{filename_prefix}-{timestamp}.png" if filename_prefix else f"{timestamp}.png"
    output_dir = os.path.expanduser(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    # 执行 adb 命令并捕获输出
    process = subprocess.Popen("adb exec-out screencap -p", shell=True, stdout=subprocess.PIPE)

    # Start loading animation
    loading = TermLoading()
    loading.show_loading()

    output, _ = process.communicate()

    # Stop loading animation
    loading.stop_loading()

    # 使用 PIL 来缩放图片
    try:
        image = Image.open(io.BytesIO(output))
    except UnidentifiedImageError:
        print("Unable to capture screenshot. The screen might be protected.")
        return
    new_size = (int(image.width * scale), int(image.height * scale))
    resized_image = image.resize(new_size, Image.ADAPTIVE)

    # 保存缩放后的图片
    with open(filepath, 'wb') as file:
        resized_image.save(file, "PNG")

    # 如果用户选择复制到剪贴板，将图片复制到剪贴板
    if copy_to_clipboard:
        # Save the image to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp:
            resized_image.save(temp.name, 'PNG')  # Use resized_image instead of image

        # Use osascript to copy the image to the clipboard
        os.system(f"osascript -e 'set the clipboard to (read (POSIX file \"{temp.name}\") as JPEG picture)'")
        print("Image copied")
    else:
        print(f"Screenshot saved as {filepath}")

if __name__ == "__main__":
    # 创建解析器
    parser = argparse.ArgumentParser(description='Capture a screenshot.')
    parser.add_argument('-n', '--name', type=str, metavar='prefix', help='the prefix of the filename')
    parser.add_argument('-s', '--scale', type=float, metavar='scale_factor', help='scale of the screenshot', default=1.0)
    parser.add_argument('-c', '--copy', action='store_true', help='copy the screenshot to clipboard', default=False)
    parser.add_argument('-o', '--out', type=str, metavar='output_dir', help='the output directory of the screenshot', default="~/Desktop")

    # 解析参数
    args = parser.parse_args()

    # 使用参数
    filename_prefix = args.name
    scale = args.scale
    copy_to_clipboard = args.copy
    output_dir = args.out

    capture_screenshot(filename_prefix, scale, copy_to_clipboard, output_dir)
    