#!/usr/bin/env python3

# 从设备上获取 apk

import argparse
import os
import subprocess

# 创建解析器
parser = argparse.ArgumentParser(description='Pull APK from device.')
parser.add_argument('pkg_name', help='The package name of the APK to pull')
parser.add_argument('-o','--out', help='The output directory to pull APK to', default='~/Desktop')

# 解析参数
args = parser.parse_args()

# 获取用户主目录的绝对路径
home_dir = os.path.expanduser('~')

# 获取 APK 路径
try:
    apk_paths = subprocess.check_output(['adb', 'shell', 'pm', 'path', args.pkg_name]).decode().splitlines()
    # 去除 'package:' 前缀
    apk_paths = [apk_path.replace('package:', '') for apk_path in apk_paths]
except subprocess.CalledProcessError as e:
    if not e.output:
        print(f"Package {args.pkg_name} not found on device")
    else:
        print(f"Error executing adb command: {e.output}")
    exit(1)

# 显示 APK 列表
print("Available APKs for package", args.pkg_name)
for i, apk_path in enumerate(apk_paths):
    print(f"[{i}] {os.path.basename(apk_path)}")

# 获取用户选择
selection = int(input("Enter the number of the APK to pull: "))

# 验证选择是否有效
if selection < 0 or selection >= len(apk_paths):
    print("Invalid selection")
    exit(1)

# 拉取 APK
apk_name = f"{args.pkg_name}-{os.path.basename(apk_paths[selection])}"
if args.out.startswith('~/'):
    destination_dir = os.path.join(home_dir, args.out.lstrip('~/'))
else:
    destination_dir = args.out

# 创建目录（如果不存在）
os.makedirs(destination_dir, exist_ok=True)

destination = os.path.join(destination_dir, apk_name)
subprocess.run(['adb', 'pull', apk_paths[selection], destination])
print(f"APK pulled to {destination}")
