import os
import sys
import re

# Database instance
class Database():
    # constructor, not used.
    def __init__(self):
        {}#TODO: constructor

    # Saves the specified file.
    def saveFile(self, file, data):
        '''(self, str, dict) -> None

        Saves (or creates) the specified file, with contents from the dict data.'''
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

    # Loads the specified file.
    def loadFile(self, file):
        '''(self, str) -> None

        Loads the data from the specified file into a new dict instance and returns it.'''
        
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
