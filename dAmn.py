import os

# dAmn Packet instance
class Packet:
    # constructor, initializes a blank packet.
    def __init__(self):
        '''(self) -> None

        Create a new, blank packet.'''
        self.command = ''
        self.subCommand = ''
        self.parameter = ''
        self.subParameter = ''
        self.body = ''
        self.raw = ''
        self.arguments = {}
        self.separator = '='

    # parse down a packet from the string-representation of the bytes.
    def parse(self, data):
        '''(self, str) -> None

        Parse down the string version of a dAmn packet into an object.'''
        
        if '\n' not in data:
            print('Attempted to parse an invalid packet: {0}'.format(data.replace('\n', '\\n')))
        else:
            data = data.replace('\0', '')
            self.raw = data.replace('\n', '\\n')
            nlPos = data.find('\n') #why make multiple calls?
            chunk = data[:nlPos]

            if ' ' in chunk:
                spPos = chunk.find(' ') #why make multiple calls?
                self.command = chunk[:spPos]
                self.parameter = chunk[spPos + 1:]
            else:
                self.command = chunk

            data = data[nlPos + 1:]

            if '\n\n' in data:
                #TODO: Tablumps!!!
                nlPos = data.find('\n\n') #why make multiple calls?
                self.body = data[nlPos + 2:]
                data = data[:nlPos]

            self.parseArgs(data)

    # parse out arguments
    def parseArgs(self, data):
        '''(self, str) -> None

        Finds and parses arguments from the specified chunk of data.'''
        
        if '\n' not in data:
            return
        else:
            chunks = data.split('\n')
            for chunk in chunks:
                if len(chunk) != 0:
                    if self.separator in chunk:
                        sepPos = chunk.find(self.separator) #why make multiple calls?
                        self.arguments[chunk[:sepPos]] = chunk[sepPos + 1:]
                    else:
                        if ' ' in chunk:
                            spPos = chunk.find(' ') #why make multiple calls?
                            self.subCommand = chunk[:spPos]
                            self.subParameter = chunk[spPos + 1:]
                        else:
                            self.subCommand = chunk
