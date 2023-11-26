#!/usr/bin/env python3

import os
import argparse
from PIL import Image

def merge_images(input_dir, output_dir, merge_mode):
    # 获取输入目录下的所有图片文件
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')]
    files.sort()  # 确保图片按照名称排序

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
    new_img.save(os.path.join(output_dir, 'merged.png'))

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

    merge_images(input_dir, output_dir, merge_mode)
    