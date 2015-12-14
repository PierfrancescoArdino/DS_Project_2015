#!/usr/bin/python 

from bank import Bank
import sys


def main():
    Bank(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))

if __name__ == '__main__':
    main()

