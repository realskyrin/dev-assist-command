#!/usr/bin/env python3

import subprocess
import sys

def get_connected_devices():
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')[1:]
    devices = [line.split('\t')[0] for line in lines if line.strip()]
    return devices

def install_apk(device, apk_path):
    result = subprocess.run(['adb', '-s', device, 'install', '-r', apk_path], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"APK 已成功安装到设备 {device}")
    else:
        print(f"安装失败: {result.stderr}")

def main():
    if len(sys.argv) < 2:
        print("使用方法: python install_apk.py <apk文件路径>")
        sys.exit(1)

    apk_path = sys.argv[1]
    devices = get_connected_devices()

    if not devices:
        print("没有找到连接的安卓设备")
        sys.exit(1)

    if len(devices) == 1:
        install_apk(devices[0], apk_path)
    else:
        print("找到多个设备:")
        for i, device in enumerate(devices):
            print(f"{i + 1}. {device}")
        
        choice = input("请选择要安装 APK 的设备 (输入序号): ")
        try:
            device_index = int(choice) - 1
            if 0 <= device_index < len(devices):
                install_apk(devices[device_index], apk_path)
            else:
                print("无效的选择")
        except ValueError:
            print("请输入有效的数字")

if __name__ == "__main__":
    main()