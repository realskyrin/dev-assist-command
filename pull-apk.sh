#!/bin/bash

# 从设备上获取 apk 文件

# 检查是否提供了包名
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <pkg name>"
    exit 1
fi

pkg_name=$1
destination_dir=~/Desktop/

# 获取 APK 路径
IFS=$'\n' apk_paths=($(adb shell pm path $pkg_name | sed 's/package://'))

# 检查是否找到了 APK
if [ ${#apk_paths[@]} -eq 0 ]; then
    echo "No APKs found for package $pkg_name"
    exit 1
fi

# 显示 APK 列表并提供选择
echo "Available APKs for package $pkg_name:"
for i in "${!apk_paths[@]}"; do
    apk_file=$(basename "${apk_paths[$i]}")
    echo "[$i] $apk_file"
done

# 获取用户选择
read -p "Enter the number of the APK to pull: " selection

# 验证选择是否有效
if [[ ! $selection =~ ^[0-9]+$ ]] || [ $selection -lt 0 ] || [ $selection -ge ${#apk_paths[@]} ]; then
    echo "Invalid selection"
    exit 1
fi

# 执行 APK 拉取
adb pull "${apk_paths[$selection]}" "$destination_dir"
echo "APK pulled to $destination_dir"
