#!/usr/bin/env python3

import os
import argparse
from PIL import Image
import time
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
        i = 0
        while True:
            while not self.__threadEvent.is_set():
                i = (i + 1) % len(emojis)
                print('\r' + emojis[i], end='', flush=True)
                time.sleep(0.1)
            print('\r', end='', flush=True)  # clear the line
            self.__threadEvent.wait()
            self.__threadEvent.clear()

def merge_images(input_dir, output_dir, merge_mode):
    # 检查输入目录是否存在
    if not os.path.exists(input_dir):
        raise Exception(f"Input directory {input_dir} does not exist.")

    # 获取输入目录下的所有图片文件
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')]
    
    # 检查是否有图片文件
    if not files:
        raise Exception(f"No image files found in the directory {input_dir}")

    files.sort()  # 确保图片按照名称排序

    # Start loading animation
    loading = TermLoading()
    loading.show_loading()

    # 读取所有图片文件
    images = [Image.open(f) for f in files]

    # 根据用户指定的合并方式进行合并
    if merge_mode == 'v':
        widths, heights = zip(*(i.size for i in images))
        total_width = max(widths)
        total_height = sum(heights)
        new_img = Image.new('RGB', (total_width, total_height))

        y_offset = 0
        for img in images:
            new_img.paste(img, (0, y_offset))
            y_offset += img.height
    else:
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        total_height = max(heights)
        new_img = Image.new('RGB', (total_width, total_height))

        x_offset = 0
        for img in images:
            new_img.paste(img, (x_offset, 0))
            x_offset += img.width

    # 保存合并后的图片到指定的输出目录
    merged_image_path = os.path.join(output_dir, 'merged.png')
    new_img.save(merged_image_path)

    # Stop loading animation
    loading.stop_loading()

    print(f"Images have been successfully merged into {merged_image_path}")
    
if __name__ == "__main__":
    # 创建解析器
    parser = argparse.ArgumentParser(description='Merge images.')
    parser.add_argument('dir', type=str, help='the directory of the images')
    parser.add_argument('-o', '--out', type=str, metavar='output_dir', help='the output directory of the merged image', default=None)
    parser.add_argument('-v', '--vertical', action='store_true', help='merge images vertically', default=False)
    parser.add_argument('-hor', '--horizontal', action='store_true', help='merge images horizontally', default=False)

    # 解析参数
    args = parser.parse_args()

    # 使用参数
    input_dir = args.dir
    output_dir = args.out if args.out else input_dir
    merge_mode = 'h' if args.horizontal else 'v' if args.vertical else 'h'

    try:
        merge_images(input_dir, output_dir, merge_mode)
    except Exception as e:
        print(e)