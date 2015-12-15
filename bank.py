#!/usr/bin/python2.7

import socket
import threading
import signal
import psutil
from bankinterfaceout import bankInterfaceOut
import time
import random

random.seed()

class Bank:


    def __init__(self, start_port, bank_number, total_banks):
        self.lock = threading.Lock()
        self.total_money = 1000
        self.bank_number = bank_number
        self.bank_interface_out_list = []
        threading.Thread(target = self.setup_server,
                                args = (start_port + bank_number,)).start()
        time.sleep(2)
        for i in xrange(0, total_banks):
            if i != bank_number:
               self.bank_interface_out_list.append(bankInterfaceOut(
                                        start_port+i, i, bank_number))
        # TODO: new tread(money sender)
        threading.Timer(int(random.uniform(2,5)), self.money_sender).start()


    def money_sender(self):
        while True:
            with self.lock:
                money = int(random.uniform(1,self.total_money))
                to_send = random.randint(0,len(self.bank_interface_out_list)-1)
                byte_sent =self.bank_interface_out_list[to_send].send_money(money)
                if byte_sent != 0:
                    self.total_money -= money
                    print "i'm " + str(self.bank_number) + " new total " +\
                            str(self.total_money)
                else:
                    print "Somethings gone wrong with bank: " + str(to_send) +" money are not transfered and connection with that bank is closed"
                    del self.bank_interface_out_list[to_send]
            time.sleep(random.randint(2,5))
        #threading.Timer(random.randint(2,5), self.money_sender).start()

    def setup_server(self, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #server_socket.bind((socket.gethostname(), port))
        server_socket.bind(('', port))
        server_socket.listen(10)

        while True:
            (client_sock, addr) = server_socket.accept()
            bank_id = int(client_sock.recv(16))
            print "i'm bank " + str(self.bank_number) + " received from " + str(bank_id)
            threading.Thread( target = self.recv_handl,
                                args = (client_sock, bank_id)).start()

    def recv_handl(self, client_sock, bank_id):
        while True:
            tmp = client_sock.recv(16)
            if tmp is not None:
                try:
                    money = int(tmp)
                    print "I'm " + str(self.bank_number) + " received from "\
                            +str(bank_id) + " euro " + str(money)
                    with self.lock:
                        self.total_money += money
                        #time.sleep(2)
                        print "I'm " + str(self.bank_number) + " new total "\
                                + str(self.total_money)

                except:
                    #is a snapshot marker
                    pass

