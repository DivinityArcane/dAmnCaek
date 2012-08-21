import os
from Database import Database
from Server import Server

#TODO: Config
if False == os.path.exists('Database/config'):
    print('Server is not configured.\n')
    # add more shit later?
    config = {'address':'127.0.0.1','port':'3900','maxConnections':'50'}
    Database.saveFile('Database/config', config)
else:
    config = Database.loadFile('Database/config')
    if config is None:
        print('Failed to load config!\n')
    else:
        print('Wee')

        serv = Server(str(config['address']),
                      int(config['port']),
                      int(config['maxConnections']))

        serv.run()
