#!/usr/bin/env python3

# 查看设备上 apk 文件的签名信息

import subprocess
import sys
import tempfile
import zipfile
import os

def get_apk_paths(package_name):
    # 获取设备上指定包名的所有 APK 路径
    cmd = ["adb", "shell", "pm", "path", package_name]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    paths = [line.split(':')[1] for line in result.stdout.splitlines() if line.startswith('package:')]
    return paths

def extract_certificate_from_apk(apk_path):
    # 提取 APK 的证书
    with tempfile.TemporaryDirectory() as temp_dir:
        # 使用 adb 拉取 APK 文件到临时目录
        local_apk_path = os.path.join(temp_dir, os.path.basename(apk_path))
        subprocess.run(["adb", "pull", apk_path, local_apk_path])

        with zipfile.ZipFile(local_apk_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        meta_inf_path = os.path.join(temp_dir, 'META-INF')
        rsa_file = next((f for f in os.listdir(meta_inf_path) if f.endswith('.RSA')), None)

        if rsa_file is None:
            print("No RSA file found in APK.")
            return

        rsa_file_path = os.path.join(meta_inf_path, rsa_file)
        cmd = ["openssl", "pkcs7", "-inform", "DER", "-text", "-print_certs", "-in", rsa_file_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.stderr:
            print("Error:", result.stderr)
            return

        print(result.stdout)

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <package_name>")
        sys.exit(1)

    package_name = sys.argv[1]
    apk_paths = get_apk_paths(package_name)

    if not apk_paths:
        print("No APK found for package:", package_name)
        return

    # 显示 APK 文件名供用户选择
    print(f"Available APKs for package {package_name}:")
    for i, path in enumerate(apk_paths, 0):
        apk_file_name = os.path.basename(path)
        print(f"[{i}] {apk_file_name}")

    choice = int(input("Enter the number of the APK to extract the certificate: "))
    if 0 <= choice < len(apk_paths):
        extract_certificate_from_apk(apk_paths[choice])
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
