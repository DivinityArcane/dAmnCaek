import os
import sys
import re

class Database():
    def __init__(self):
        {}#TODO: constructor
        
    def saveFile(self, file, data):
        if isinstance(data, dict):
            try:
                fileName = re.sub(r'[^a-zA-Z0-9/]*', '', file)
                fileData = ''
                for key in data:
                    fileData += '{0}={1}\0'.format(str(key), str(data[key]))
                fileHandle = open(fileName, 'w+')
                if fileHandle:
                    fileHandle.write(fileData)
                    fileHandle.close()
                else:
                    print('Error @ Database.SaveFile: could not open file for writing: {0}'.format(fileName))
            except:
                print('Error @ Database.SaveFile: {0}'.format(sys.exc_info()[0]))
        else:
            print('Error @ Database.SaveFile: data must be a dictionary.')

    def loadFile(self, file):
        if os.path.exists(file):
            try:
                fileName = re.sub(r'[^a-zA-Z0-9/]*', '', file)
                fileData = {}
                handle = open(fileName, 'r')
                if handle:
                    tmp = handle.read().split('\0')
                    for line in tmp:
                        if len(line) >= 3 and '=' in line:
                            sepPos = line.find('=')
                            key = line[:sepPos].strip()
                            value = line[sepPos + 1:].strip()
                            fileData[key] = value
                    handle.close()
                    return fileData
                else:
                    print('Error @ Database.LoadFile: could not open file for reading: {0}'.format(fileName))
            except:
                print('Error @ Database.LoadFile: {0}'.format(sys.exc_info()[0]))
        else:
            print('Error @ Database.LoadFile: file does not exist: {0}'.format(file))
