#!/usr/bin/python2.7

# This class provides pkt_handler for money and snapshot, start the snapshot and implements the money transfert logic

import socket
import threading
import signal
import psutil
from bankinterfaceout import bankInterfaceOut
import time
import random

random.seed()

class Bank:

    def __init__(self, host, port, flag_snapshot):
        self.lock = threading.Lock()
        self.total_money = 1000000
        self.bank_number = host + ':' + str(port)
        self.bank_list = self.__parse_host_file()
        self.bank_interface_out_list = []
        """
        is None if the bank is not in snapshot mode
        contain current snapshot ID otherwhise
        """
        self.snapshot_mode = None
        self.snapshot_internal_state = None
        self.snapshot_received_money = 0
        #self.snapshot_token_received = [False] * len(self.bank_list)
        threading.Thread(target = self.setup_server,
                                args = (int(port),)).start()
        if flag_snapshot == '1':
            threading.Timer(7,self.start_snapshot).start()

        time.sleep(2)
        for i in self.bank_list:
            if self.bank_number != i['id']:
                self.bank_interface_out_list.append(bankInterfaceOut(
                    i['host'], i['port'], i['id'], self.bank_number))
            else:
                i['token_received'] = True
        # TODO: new tread(money sender)
        threading.Timer(int(random.uniform(2,5)), self.money_sender).start()


    def money_sender(self):
        while True:
            with self.lock:
                if self.total_money != 0:
                    money = int(random.uniform(1,min(100,self.total_money)))
                    to_send = random.randint(0,len(self.bank_interface_out_list)-1)
                    byte_sent =self.bank_interface_out_list[to_send].send_money(money)
                    if byte_sent != 0:
                        self.total_money -= money
                        print "i'm " + str(self.bank_number) + " new total " +\
                                str(self.total_money)
                    else:
                        print "Somethings gone wrong with bank: " + str(to_send) +\
                            " money are not transfered and connection with\
                            that bank is closed"
                        del self.bank_interface_out_list[to_send]
            #time.sleep(random.randint(2,5))
        #threading.Timer(random.randint(2,5), self.money_sender).start()

    def setup_server(self, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #server_socket.bind((socket.gethostname(), port))
        server_socket.bind(('', port))
        server_socket.listen(10)

        while True:
            (client_sock, addr) = server_socket.accept()
            bank_id = client_sock.recv(32).lstrip()
            print "i'm bank " + str(self.bank_number) + " received from " + str(bank_id)
            threading.Thread( target = self.recv_handl,
                                args = (client_sock, bank_id)).start()

    def recv_handl(self, client_sock, bank_id):
        while True:
            tmp = client_sock.recv(16)
            if tmp is not None:
                self.pkt_handler(tmp, bank_id)

    def pkt_handler(self, pkt, bank_id):
        if pkt[0:1] != "S":#is a normal money transfer
            money = int(pkt)
            self.money_pkt_handler(money, bank_id)

        else:
            self.snapshot_pkt_handler(int(pkt[1:]), bank_id)

    def money_pkt_handler(self, money, bank_id):
        with self.lock:
            print "I'm " + str(self.bank_number) + " received from "\
                    +str(bank_id) + " euro " + str(money)
            self.total_money += money
            #time.sleep(2)
            print "I'm " + str(self.bank_number) + " new total "\
                    + str(self.total_money)
            if self.snapshot_mode != None:
                for i in self.bank_list:
                    if (not i['token_received']) and i['id'] == bank_id:
                        self.snapshot_received_money += money

    def snapshot_pkt_handler(self, snapshot_id, bank_id):
        with self.lock:
            print "@bank "+self.bank_number + " received token from "+ bank_id
            if self.snapshot_mode is None:
                #time.sleep(1)
                self.snapshot_received_money = 0
                self.snapshot_mode = snapshot_id
                self.snapshot_internal_state = self.total_money
                for i in self.bank_list:
                    if i['id'] != self.bank_number:
                        i['token_received'] = False
                for i in self.bank_interface_out_list:
                    i.send_token(snapshot_id)
            tmp_flag = True
            for i in self.bank_list:
                if i['id'].lstrip() == bank_id.lstrip():
                    i['token_received'] = True
                tmp_flag = tmp_flag and i['token_received']

            if tmp_flag and (self.snapshot_mode is not None):
                #finish snapshot
                self.snapshot_mode = None
                print "@snapshot %s finished on bank %s " % (snapshot_id, self.bank_number)
                print "@internal state %s money received during snapshot %s" %\
                (self.snapshot_internal_state,
                        self.snapshot_received_money)
                #save log
                with open("./logs/" + self.bank_number + ".log", 'a') as log:
                    log.write(str(snapshot_id) + ' ' + str(self.snapshot_internal_state) + \
                            ' ' + str(self.snapshot_received_money) + '\n')



    def start_snapshot(self):
        snapshot_progressive_id = 0
        while True:
            if self.snapshot_mode is None:
                with self.lock:
                    snapshot_progressive_id += 1
                    self.snapshot_received_money = 0
                    self.snapshot_mode = snapshot_progressive_id
                    self.snapshot_internal_state = self.total_money
                    for i in self.bank_list:
                        if i['id'] != self.bank_number:
                            i['token_received'] = False
                        else:
                            i['token_received'] = True
                    for i in self.bank_interface_out_list:
                        #time.sleep(3)
                        i.send_token(snapshot_progressive_id)
            time.sleep(5)


    def __parse_host_file(self):

        #get list of banks
        with open('./host.list','r') as bank_file:
            tmp = bank_file.read().splitlines()

        #split hostname and port
        bank_list = []
        for line in tmp:
            d = {}
            parsed_line = line.rsplit(':')
            d['host'] = parsed_line[0]
            d['port'] = parsed_line[1]
            d['id'] = d['host'] + ':' + d['port']
            d['port'] = int(d['port'])
            d['token_received'] = False
            bank_list.append(d)
        return bank_list

