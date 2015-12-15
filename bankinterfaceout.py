#!/usr/bin/python2.7
import socket

class bankInterfaceOut:

    def __init__(self, bank_port, bank_id, my_id):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #FIXME add host param
        print "i'm bank " + str(my_id) + " try to connect to " + str(bank_port)
        self.sock.connect(("127.0.0.1", bank_port))
        self.bank_id = bank_id
        self.sock.send(str(my_id))

