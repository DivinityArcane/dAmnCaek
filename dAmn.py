import os

class Packet:
    def __init__(self):
        self.command = ''
        self.subCommand = ''
        self.parameter = ''
        self.subParameter = ''
        self.body = ''
        self.raw = ''
        self.arguments = {}
        self.separator = '='

    def parse(self, data):
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


    def parseArgs(self, data):
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
