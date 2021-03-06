#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
from multiprocessing import cpu_count

import psutil

cpu_core_count = cpu_count()  # CPU 核心数量


def get_process_by_id(arg_pid):
    return psutil.Process(arg_pid)


def get_process_by_name(arg_name):
    for p in psutil.process_iter():
        try:
            if p.name().lower() == arg_name.lower():
                return p
        except psutil.AccessDenied as e:
            print("权限不足")
            return None
        except psutil.NoSuchProcess as e:
            print("没有找到该进程")
            return None
    return None


def get_cpu_info(arg_proc, arg_interval):
    cpu_info = {}
    cpu_info['percent'] = arg_proc.cpu_percent(interval=int(arg_interval)) / cpu_core_count
    return cpu_info


def print_help():
    print(u"用法 python get_process_memory_info.py -p ... [-t ... -l ...]")
    print(u"选项：")
    print(u"\t -h/--help 帮助")
    print(u"\t -p 进程名")
    print(u"\t -t 检测时间间隔[可选参数]")
    print(u"\t -l 日志文件路径[可选参数]")


def get_argvs():
    global argv_process_name
    global argv_time_interval
    global argv_log_path
    count = 1
    while count < len(sys.argv):
        if sys.argv[count] == "-h" or sys.argv[count] == "--help":
            print_help()
            sys.exit(0)
        if sys.argv[count] == "-p":
            count += 1
            if count < len(sys.argv):
                argv_process_name = sys.argv[count]

        if sys.argv[count] == "-t":
            count += 1
            if count < len(sys.argv):
                argv_time_interval = sys.argv[count]

        if sys.argv[count] == "-l":
            count += 1
            if count < len(sys.argv):
                argv_log_path = sys.argv[count]
        count += 1


if __name__ == '__main__':
    argv_process_name = ""
    argv_time_interval = ""
    argv_log_path = ""

    get_argvs()

    if argv_process_name == "":
        print_help()
        sys.exit(0)

    if argv_time_interval == "":
        argv_time_interval = 1
        print("时间间隔为空，使用默认值1秒")

    if argv_log_path == "":
        argv_log_path = "./"
        print("日志路径为空，使用默认值当前路径")

    process = get_process_by_name(argv_process_name)

    if process is not None:
        while True:
            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            cpu_info = get_cpu_info(process, argv_time_interval)

            with open(os.path.join(argv_log_path, argv_process_name[:-4] + "_cpu.log"), "a") as f:
                write_str = '[' + str(now_time) + ']|{"cpu":"' + str(cpu_info['percent']) + '%' + '"}\n'
                print(write_str)
                f.write(write_str)
    else:
        print("没有找到该进程: " + argv_process_name)
        sys.exit(0)
