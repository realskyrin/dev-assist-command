#!/usr/bin/env python3

import subprocess

def get_device_info():
    model = subprocess.getoutput('adb shell getprop ro.product.model').strip()
    android_version = subprocess.getoutput('adb shell getprop ro.build.version.release').strip()
    screen_resolution = subprocess.getoutput('adb shell wm size').strip().split(": ")[1]
    dpi = subprocess.getoutput('adb shell getprop ro.sf.lcd_density').strip()
    refresh_rate = subprocess.getoutput('adb shell dumpsys display | grep mBaseDisplayInfo').strip().split(", ")[4]
    cpu_abi = subprocess.getoutput('adb shell getprop ro.product.cpu.abi').strip()
    cpu_bit = subprocess.getoutput('adb shell getprop ro.zygote').strip()
    gpu_version = subprocess.getoutput('adb shell getprop ro.opengles.version').strip()
    language = subprocess.getoutput('adb shell getprop user.language').strip()
    timezone = subprocess.getoutput('adb shell getprop persist.sys.timezone').strip()
    is_root = 'Yes' if 'uid=0(root)' in subprocess.getoutput('adb shell su -c id').strip() else 'No'

    print(f"Model: {model}")
    print(f"Android Version: {android_version}")
    print(f"Screen Resolution: {screen_resolution}")
    print(f"DPI: {dpi}")
    print(f"Refresh Rate: {refresh_rate}")
    print(f"CPU ABI: {cpu_abi}")
    print(f"CPU Bit: {cpu_bit}")
    print(f"GPU Version: {gpu_version}")
    print(f"Language: {language}")
    print(f"Timezone: {timezone}")
    print(f"Is Root: {is_root}")

if __name__ == "__main__":
    get_device_info()
    