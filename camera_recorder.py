#!/usr/bin/python
from pathlib import Path
import os
import shutil
import subprocess

work_dir_path = '/home/camera/records'
video_dur_msec = 60000

work_dir = Path(work_dir_path)


def clean_lower_than_num(w_d, num):
    for child in w_d.iterdir():
        cur_num = int(child.name.split('_')[0])
        if cur_num < num:
            os.remove(child)


def find_biggest_number(w_d):
    num = 0
    for child in w_d.iterdir():
        candidate = int(child.name.split('_')[0])
        if candidate > num:
            num = candidate
    return num


def record_video(w_d, num):
    # Run a command and wait for it to finish
    result = subprocess.run(
        ["raspivid",
         "-o", w_d.joinpath(f"{num}_video.h264"),
         "-t", str(video_dur_msec),
         "-w", "1280",
         "-h", "720",
         "-fps", "24"],
         capture_output=True,
         text=True)
    print(f"stdout: {result.stdout}")
    print(f"stderr: {result.stderr}")


def main():
    num = find_biggest_number(work_dir)
    num += 1
    # clean space
    total, used, free = shutil.disk_usage('/')
    free_gbs = free / (1024**3)
    if free_gbs < 1:
        clean_lower_than_num(work_dir, num)

    while True:
        # record the video
        print(f'Start record video: {num}')
        record_video(work_dir, num)
        num += 1

if __name__ == "__main__":
    main()
