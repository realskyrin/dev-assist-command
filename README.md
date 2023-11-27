# dev-assist-command
Some scripts to assist development

English/[简体中文](./README-zh.md)

## Requirements

- Python/Python3 installed, some scripts may need to be executed in a Python environment
```shell
➜  ~  python3 // Check if Python is installed
Python 3.9.6 (default, Aug 11 2023, 19:44:49) 
[Clang 15.0.0 (clang-1500.0.40.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
```

- Correctly configured adb path in the environment variables, some tasks may need to be executed in an adb environment
```shell
➜  ~  adb // Check if adb is installed
Android Debug Bridge version 1.0.41
Version 34.0.4-10411341
Installed as ~/Library/Android/sdk/platform-tools/adb
Running on Darwin 22.6.0 (arm64)
```

## Usage

- Run py scripts
```shell
python/python3 xxx.py -h
```

- Run shell scripts
```shell
chmod +x xxx.sh // Grant execution permissions to the sh script
./xxx.sh <param>
```

## Command Wrapper

To more conveniently run functions directly after starting the terminal, you can create a `cmd-wrapper.sh`, define the script references and calling methods in it, and initialize it in `.zprofile`:

Create `cmd-wrapper.sh` and add the following content
```bash
#!/bin/bash

fun cap(){
    python/python3 ~/code/dev-assist-command/screenshot.py "$@"
}
```

Append in `.zprofile` file (located at ~/.zprofile)
```bash
# cmd-wrapper utils
source <path>/cmd-wrapper.sh
```

After restarting the terminal, you can directly run the script
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
