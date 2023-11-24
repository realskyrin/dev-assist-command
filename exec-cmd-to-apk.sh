#!/bin/bash

# 对设备上的 apk 文件执行 java 命令

# 检查是否提供了足够的参数
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <path to jar> <pkg name>"
    exit 1
fi

jar_path=$1
pkg_name=$2
temp_dir="/tmp/apk_temp_dir"

# 确保临时目录存在
mkdir -p "$temp_dir"

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
read -p "Enter the number of the APK to use: " selection

# 验证选择是否有效
if [[ ! $selection =~ ^[0-9]+$ ]] || [ $selection -lt 0 ] || [ $selection -ge ${#apk_paths[@]} ]; then
    echo "Invalid selection"
    exit 1
fi

# 拉取 APK 到临时目录
adb pull "${apk_paths[$selection]}" "$temp_dir"

# 获取拉取的 APK 文件的本地路径
local_apk_path="$temp_dir/$(basename "${apk_paths[$selection]}")"

# 执行 java 命令
java -jar "$jar_path" "$local_apk_path"
echo "Command executed on the APK at $local_apk_path"

# 删除 APK 文件
rm "$local_apk_path"
echo "APK file removed from $temp_dir"