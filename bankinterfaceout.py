#!/usr/bin/python2.7


# This class provides communication interface through two bank.
# init function: provides connection to another bank.
# Provides 2 methods:
# send_money(amount): send money to the other bank
# send_token(snapshot_id): send snapshot token to the other bank


import socket
import errno
import time
from socket import error as socket_error
class bankInterfaceOut():
    #connected = False
    def __init__(self, host, port, bank_id, my_id):
        connected = False
        self.bank_host = host
        self.bank_port = port
        self.bank_id = bank_id
        self.my_id = my_id
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #FIXME add host param
        while (connected is not True):
            try:
                print "i'm bank " + str(my_id) + " try to connect to " + str(self.bank_port)
                self.sock.connect((self.bank_host, self.bank_port))
                connected = True
            except socket_error as serr:
                print "somethings gone wrong, i'm trying to connect again in 2 seconds"
                time.sleep(2)
        self.sock.send('%32s' % (self.my_id))

    def send_money(self, amount):
        attempt = 0
        b_sent = 0
        while attempt < 3:
            try:
                b_sent = self.sock.send('%16s' % (amount))
                attempt = 4
            except socket_error as serr:
                print "@@somethings gone wrong during the send, bank "\
                        +str(self.my_id) + " donesn't responds i'm \
                        trying to send again in 2 seconds"
                time.sleep(2)
                attempt += 1
                b_sent = 0
        return b_sent
    def send_token(self, snapshot_id):
        attempt = 0
        b_sent = 0
        while attempt < 3:
            try:
                b_sent = self.sock.send('S%15s' % (snapshot_id))
                attempt = 4
            except socket_error as serr:
                print "@@somethings gone wrong during the send of token, bank "\
                        +str(self.my_id) + " donesn't responds i'm \
                        trying to send again in 2 seconds"
                time.sleep(2)
                attempt += 1
                b_sent = 0
        return b_sent
    def get_bank_id(self):
        return self.bank_id
