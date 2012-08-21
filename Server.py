import socket
import sys 
import threading 
from Client import Client

class Server():
    def __init__(self, ip, port, maxCn):
        self.ip = ip
        self.port = port
        self.maxConnections = maxCn
        self.clients = {}
        self.threadPool = []
        self.clientCount = 0
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((ip, port))
            self.sock.listen(self.maxConnections)
            if self.sock:
                print('Woot! We established the socket on {0}:{1}\n'.format(self.ip ,self.port))
        except:
            print('Error while setting up server: {0}\n'.format(sys.exc_info()[0]))
            return

    def run(self):
        self.running = True

        while self.running:
            (clientSock, clientAddr) = self.sock.accept()
            self.clientCount += 1
            client = Client(self, clientSock, clientAddr)
            client.run()
            self.threadPool.append(client)

        self.sock.close()
        for thread in self.threadPool:
            thread.join()
