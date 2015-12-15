#!/usr/bin/python2.7
import socket
import errno
import time
from socket import error as socket_error
class bankInterfaceOut():
    #connected = False
    def __init__(self, bank_port, bank_id, my_id):
        connected = False
        self.bank_port = bank_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #FIXME add host param
        while (connected is not True):
            try:
                print "i'm bank " + str(my_id) + " try to connect to " + str(self.bank_port)
                self.sock.connect(("127.0.0.1", self.bank_port))
                connected = True
            except socket_error as serr:
                print "somethings gone wrong, i'm trying to connect again in 2 seconds"
                time.sleep(2)
        self.bank_id = bank_id
        self.sock.send('%16s' % (my_id))

    def send_money(self, amount):
        attempt = 0
        b_sent = 0
        while attempt < 3:
            try:
                b_sent = self.sock.send('%16s' % (amount))
                attempt = 4
            except socket_error as serr:
                print "somethings gone wrong during the send, bank "+str(self.bank_id) + " donesn't responds i'm trying to connect again in 2 seconds"
                time.sleep(2)
                attempt += 1
                b_sent = 0
        return b_sent
    def start_snapshot(self):
        pass
