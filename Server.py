import socket
import sys 
from _thread import start_new_thread, allocate_lock
from Client import Client
import traceback

# Server class/instance
class Server():
    # constructor, initiate the instance.
    def __init__(self, ip, port, maxCn):
        '''(self, str, int, int) -> None

        Creates a new server instance.'''
        self.ip = ip
        self.port = port
        self.maxConnections = maxCn
        self.clients = {}
        self.channels = {}
        self.clientCount = 0
        self.lock = allocate_lock()
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
        '''(self) -> None

        Start running the server and waiting for connections. On connect,
        process the connection(s).'''
        # if the server failed to load 
        # it wont attempt this, which would only return another traceback. so yeah :P
        while self.running:
            try:            
                (clientSock, clientAddr) = self.sock.accept()
                self.clientCount += 1
                client = start_new_thread(Client, (self, clientSock, clientAddr))
            except KeyboardInterrupt:
                print("Server stopped [Keyboard interrupt]")
                self.running = False
        print('Server has stopped running, killing threads.')
        self.sock.close()
