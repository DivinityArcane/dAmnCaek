import socket
import sys
import time
import threading
import dAmn

class Client(threading.Thread):

    def __init__(self, parent, sock, clientAddr):
        threading.Thread.__init__(self)
        self.username = ''
        self.realname = 'dAmnCaek Supporter'
        self.typename = 'dAmnCaek Client'
        self.gpc = 'guest'
        self.symbol = '='
        self.channels = []
        self.server = parent #we will need this ref later
        self.sock = sock
        self.addr = clientAddr
        self.loggedIn = False
        self.running = True
        self.lastPing = time.time()
        self.lastPong = time.time()
        self.bufferSize = 1 #it's easier lol
        print('Client incoming: {0}'.format(self.addr))
        self.run()

    def loginCheck(self):
        if False == self.loggedIn:
            try:
                self.disconnect('no login')
                self.running = False
            except:
                self.running = False

    def pingPong(self):
        if time.time() - self.lastPong > 60:
            self.disconnect('timed out')
        else:
            self.send('ping\n\0')
            self.lastPing = time.time()
            threading.Timer(60, self.pingPong, ()).start()

    def run(self):
        if self.server.clientCount > self.server.maxConnections:
            self.disconnect('server busy')
            return
        
        data = ''

        threading.Timer(15, self.loginCheck, ()).start()

        while self.running:
            try:
                buffer = self.sock.recv(self.bufferSize)
                if buffer:
                    try:
                        data += buffer.decode("utf-8")
                        if data.endswith('\0'):
                            self.process(data)
                            data = ''
                    except:
                        print('Something went wrong while trying to read data.')
                        self.disconnect('bad data')
                        self.sock.close()
                        self.running = False
                else:
                    self.sock.close()
                    self.running = False
            except:
                print('Client error, killing thread.')
                self.running = False

        print('Client disconnected: {0}'.format(self.addr))
        self.server.clientCount -= 1
        if self.loggedIn and self.username.lower() in self.server.clients: #bloody well should be
            del self.server.clients[self.username.lower()]

    def send(self, data):
        try:
            self.sock.sendall(bytes(data, 'utf-8'))
        except:
            self.running = False

    def disconnect(self, reason):
        self.send('disconnect\ne={0}\n\0'.format(reason))
        try:
            self.sock.close()
            self.running = False
        except:
            self.running = False

    def process(self, data):
        packet = dAmn.Packet()
        packet.parse(data)
        if packet.command == 'dAmnClient':
            if packet.parameter == '0.3':
                self.send('dAmnServer 0.3\n\0')
            else:
                self.disconnect('unsupported dAmnClient version')
        elif packet.command == 'login':
            if len(packet.parameter) > 0:
                self.username = packet.parameter
                #TODO: Check authtoken!
                #something like if packet.arguments['pk'] == sometokenfromthedb:
                if self.username.lower() == 'core':
                    self.disconnect('invalid username')
                elif self.username.lower() in self.server.clients:
                    self.disconnect('too many connections')
                else:
                    print('Client {0} has logged in as {1}'.format(self.addr, self.username))
                    self.server.clients[self.username.lower()] = self
                    self.loggedIn = True
                    self.send('login {0}\ne=ok\n\nsymbol={1}\nrealname={2}\ntypename={3}\ngpc={4}\n\0'.format(self.username, self.symbol, self.realname, self.typename, self.gpc))
                    threading.Timer(10, self.pingPong, ()).start()
            else:
                self.disconnect('no login')
        elif packet.command == 'pong':
            self.lastPong = time.time()
        elif packet.command == 'join':
            if packet.parameter.startswith('chat:'):
                chan = packet.parameter[5:].lower()
                if chan not in self.server.channels:
                    self.send('join {0}\ne=chatroom doesn\'t exist\n\0'.format(packet.parameter))
                else:
                    self.channels.append(chan)
                    self.send('join {0}\ne=ok\n\0'.format(packet.parameter))
                    self.send('property {0}\np=title\nby=core\nts=0\n\nthis is a title\n\0'.format(packet.parameter))
                    self.send('property {0}\np=topic\nby=core\nts=0\n\nthis is a topic\n\0'.format(packet.parameter))
                    self.send('property {0}\np=privclasses\n\n1=Guests\n\0'.format(packet.parameter))
                    self.send('property {0}\np=members\n\nlol\n\0'.format(packet.parameter))
            else:
                self.send('join {0}\ne=chatroom doesn\'t exist\n\0'.format(packet.parameter))
        else:
            print('Unknown packet type: {0}'.format(packet.command))
