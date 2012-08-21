import socket
import sys 
import threading

class Client(threading.Thread):

    def __init__(self, parent, sock, clientAddr):
        threading.Thread.__init__(self)
        self.server = parent #we will need this ref later
        self.sock = sock
        self.addr = clientAddr
        self.bufferSize = 1 #it's easier lol
        print('Client incoming: {0}'.format(self.addr))

    def run(self):
        if self.server.clientCount > self.server.maxConnections:
            self.sock.sendall(bytes('disconnect\ne=Server too busy\n\0', 'utf-8'))
            self.sock.close()
            return
        
        self.running = True
        data = ''

        while self.running:
            buffer = self.sock.recv(self.bufferSize)
            if buffer:
                try:
                    data += buffer.decode("utf-8")
                    if data.endswith('\0'):
                        self.process(data)
                        data = ''
                except:
                    self.sock.sendall(bytes('disconnect\ne=bad data\n\0', 'utf-8'))
                    self.sock.close()
                    self.running = False
            else:
                self.sock.close()
                self.running = False

    def process(self, data):
        #TODO: Handle packets!
        print('Unhandled packet: {0}'.format(data.replace('\n', '\\n')))
        self.sock.sendall(bytes('disconnect\ne=TODO: Handle packets!\n\0', 'utf-8'))
        self.sock.close()
        self.running = False
