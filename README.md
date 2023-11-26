# dev-assist-command
Some scripts to assist development

## Requirements

- 安装了 python/python3，一些脚本可能需要在 python 环境下执行
```shell
➜  ~  python3 // 查看 python 是否安装
Python 3.9.6 (default, Aug 11 2023, 19:44:49) 
[Clang 15.0.0 (clang-1500.0.40.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
```

- 在环境变量中正确配置了 adb path，一些任务可能需要在 adb 环境下执行
```shell
➜  ~  adb // 查看 adb 是否安装
Android Debug Bridge version 1.0.41
Version 34.0.4-10411341
Installed as ~/Library/Android/sdk/platform-tools/adb
Running on Darwin 22.6.0 (arm64)
```

## Usage

- 运行 py 脚本
```shell
python/python3 xxx.py -h
```

- 运行 shell 脚本
```shell
chmod +x xxx.sh // 赋予 sh 脚本执行权限
./xxx.sh <param>
```

## Command Wrapper

为了更方便的在 terminal 启动后可以直接运行函数，你可以创建一个 cmd-wrapper.sh 在其中定义脚本的引用以及调用方式，并在 .zprofile 中进行初始化：

创建 cmd-wrapper.sh 并添加如下内容
```bash
#!/bin/bash

fun cap(){
    python/python3 ~/code/dev-assist-command/screenshot.py "$@"
}
```

在 .zprofile（位于 ~/.zprofile） 文件中追加
```bash
# cmd-wrapper utils
source <path>/cmd-wrapper.sh
```

重启 terminal 后即可直接运行脚本
```shell
➜  ~ cap -h
usage: screenshot.py [-h] [-n prefix] [-s scale_factor] [-c] [-o output_dir]

Capture a screenshot.

options:
  -h, --help            show this help message and exit
  -n prefix, --name prefix
                        the prefix of the filename
  -s scale_factor, --scale scale_factor
                        scale of the screenshot
  -c, --copy            copy the screenshot to clipboard
  -o output_dir, --out output_dir
                        the output directory of the screenshot
```
