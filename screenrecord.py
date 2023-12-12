#!/usr/bin/env python3

import subprocess
import threading
from threading import Thread, Event
import argparse
from datetime import datetime
import os
import time

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

def record_screen(output_path):
    # Start recording
    record_process = subprocess.Popen('adb shell screenrecord /sdcard/screen.mp4', shell=True)

    # Start loading animation
    loading = TermLoading()
    loading.show_loading()

    try:
        # Wait for the recording to be stopped by the user
        print("Press Control + C to stop recording")
        record_process.wait()
    except KeyboardInterrupt:
        # Stop recording
        record_process.terminate()
        record_process.wait()

        # Stop loading animation
        loading.stop_loading()

        print("Recording stopped")

    # Pull the recorded video to the specified directory
    subprocess.run(f'adb pull /sdcard/screen.mp4 {output_path}', shell=True)

def main():
    parser = argparse.ArgumentParser(description='Record screen of Android device.')
    parser.add_argument('-o', '--out', type=str,  default="~/Desktop",
                        help='Output path for the recorded video')
    args = parser.parse_args()

    record_screen(args.out)

if __name__ == "__main__":
    main()
