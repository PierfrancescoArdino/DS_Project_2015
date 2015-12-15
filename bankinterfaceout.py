#!/usr/bin/python2.7
import socket
import errno
import time
from socket import error as socket_error
class bankInterfaceOut:
    #connected = False
    def __init__(self, bank_port, bank_id, my_id):
        connected = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #FIXME add host param
        while (connected is not True):
            try:
                print "i'm bank " + str(my_id) + " try to connect to " + str(bank_port)
                self.sock.connect(("127.0.0.1", bank_port))
                connected = True
            except socket_error as serr:
                print "somethings gone wrong, i'm trying to connect again in 2 seconds"
                time.sleep(2)
        self.bank_id = bank_id
        self.sock.send('%16s' % (my_id))
    
    def send_money(self, amount):
        self.sock.send('%16s' % (amount))

    def start_snapshot(self):
        pass
