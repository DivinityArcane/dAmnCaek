import socket
import sys 
import threading 
from Client import Client
# Modified 8/22/2012
#
# try a more direct error handling method. for the hell of it. 
import traceback

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
                print('Woot! We established the socket on {0}:{1}'.format(self.ip ,self.port))
                #server loaded and is working. so self.running = True                
                self.running = True
        except:            
            if socket.error:            
                print('Socket Error while setting up server: {0}'.format(traceback.format_exc().splitlines()[-1]))
            else: print('Error while setting up server:\n{0}'.format(traceback.format_exc()))            
            #something has gone wrong, so self.running = False
            self.running = False
            return
            

    def run(self):
        # if the server failed to load 
        # it wont attempt this, which would only return another traceback. so yeah :P
        while self.running:
            try:            
                (clientSock, clientAddr) = self.sock.accept()
                self.clientCount += 1
                client = Client(self, clientSock, clientAddr)
                client.run()
                self.threadPool.append(client)
            except KeyboardInterrupt:
                print("Server stopped [Keyboard interrupt]")
                self.running = False
        self.sock.close()
        for thread in self.threadPool:
            thread.join()
