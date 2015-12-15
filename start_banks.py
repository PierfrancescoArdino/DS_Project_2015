#!/usr/bin/python2.7

from bank import Bank
import subprocess
import time
import signal
import os
import psutil

START_PORT = 9000
NUMBER_OF_BANKS = 4


def kill_all(s, frame):
        proc_pid = os.getpid()
        process = psutil.Process(proc_pid)
        for proc in process.children(recursive=True):
            try:
                proc.kill()
                #os.kill(proc.pid, signal.SIGINT)
            except psutil.NoSuchProcess:
                pass
        if psutil.pid_exists(process.pid):
            try:
                process.kill()
            except psutil.NoSuchProcess:
                pass

signal.signal(signal.SIGINT, kill_all)
#signal.signal(signal.SIGKILL, kill_all)
#signal.signal(signal.SIGTERM, kill_all)

for i in xrange(0, NUMBER_OF_BANKS):
    subprocess.Popen(["./bank_main.py",str(START_PORT),str(i),
                                    str(NUMBER_OF_BANKS)])

while True:
    time.sleep(1)
