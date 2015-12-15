#!/usr/bin/python

import socket
import threading
import signal
import psutil
from bankinterfaceout import bankInterfaceOut
import time

class Bank:
    

    def __init__(self, start_port, bank_number, total_banks):
        self.bank_interface_out_list = []
        threading.Thread(target = self.setup_server, 
                                args = (start_port + bank_number,)).start()
        time.sleep(2)
        for i in xrange(0, total_banks):
            if i != bank_number:
                self.bank_interface_out_list.append(bankInterfaceOut(
                                        start_port+i, i, bank_number))


    def setup_server(self, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #server_socket.bind((socket.gethostname(), port))
        server_socket.bind(('', port))
        print "bind " + str( port)
        server_socket.listen(10)

        while True:
            (client_sock, addr) = server_socket.accept()
            bank_id = client_sock.recv(16)
            print "first receiv " +bank_id
            threading.Thread( target = self.recv_handl,
                                args = (client_sock, bank_id)).start()

    def recv_handl(self, client_sock, bank_id):
        print "bank id: " + bank_id
        while True:
            tmp = client_sock.recv(16)
            if tmp is not None:
                print "received" +tmp

