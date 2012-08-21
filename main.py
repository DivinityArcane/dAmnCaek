import os
from Database import Database

#TODO: Config
if False == os.path.exists('Database/config'):
    print('Server is not configured.\n')
    # add more shit later?
    test = {'address':'127.0.0.1','port':'3900','maxConnections':'50'}
    Database.saveFile('Database/config', test)
else:
    test = Database.loadFile('Database/config')
    if test is None:
        print('Failed to load config!\n')
    else:
        print('Wee')
        for key in test:
            print('{0}={1}\n'.format(key, test[key]))
