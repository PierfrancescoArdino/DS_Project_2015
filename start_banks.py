#!/usr/bin/python2.7

from bank import Bank
import subprocess

START_PORT = 9000
NUMBER_OF_BANKS = 4


for i in xrange(0, NUMBER_OF_BANKS):
    subprocess.Popen(["./bank_main.py",str(START_PORT),str(i),
                                    str(NUMBER_OF_BANKS)])

