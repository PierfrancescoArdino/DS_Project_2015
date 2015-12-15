#!/usr/bin/python2.7

#call with ./start_banks.py hostname

from bank import Bank
import subprocess
import time
import signal
import os
import sys
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

#get list of banks
with open('./host.list','r') as bank_file:
   tmp = bank_file.read().splitlines()

#split hostname and port
bank_list = []
for line in tmp:
    d = {}
    d['host'], d['port'] = line.split(':')
    bank_list.append(d)

for bank in bank_list:
    #if is a bank of this host
    if bank['host'] == sys.argv[1]:
        subprocess.Popen(['./bank_main.py', str(bank['host']),
                                        str(bank['port'])])

while True:
    time.sleep(1)
