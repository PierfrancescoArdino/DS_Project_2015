#!/usr/bin/python2.7

# This script start one bank instance

from bank import Bank
import sys


def main():
    Bank(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()

