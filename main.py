import os
from Database import Database
from Server import Server

print('dAmnCaek version 0.1 booting up...')

#TODO: Config
if False == os.path.exists('Database/config'):
    print('Server is not configured.')
    # add more shit later?
    config = {'address':'127.0.0.1','port':'3900','maxConnections':'50'}
    Database.saveFile('Database/config', config)
else:
    print('Attempting to load server configuration...')
    config = Database.loadFile('Database/config')
    if config is None:
        print('Failed to load config!')
    else:
        print('Config loaded!')
        print('Starting server...')

        serv = Server(str(config['address']),
                      int(config['port']),
                      int(config['maxConnections']))

        serv.run()
