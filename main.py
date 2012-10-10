import os
from Database import Database
from Server import Server

print('dAmnCaek version 0.1 booting up...')
db = Database()

if False == os.path.exists('Database/config'):
    print('Server is not configured.')
    print('I\'ll need to ask you a few questions to get things running.')
    
    address = input('What IP will the server run on? [127.0.0.1]: ')
    if len(address) < 7:
        address = '127.0.0.1'
        
    port = input('What port should the server run on? [3900]: ')
    if len(port) == 0:
        port = 3900
    else:
        port = int(port)
        
    max_connections = input('How many people can be connected at once? [50]: ')
    if len(max_connections) == 0:
        max_connections = 50
    else:
        max_connections = int(max_connections)
        
    print('Gotcha. So the server will run on {0}:{1}, and accept up to {2} people at once.'.format(address, port, max_connections))
    print('Saving config and closing the server, please restart.')
    
    config = {'address':address,'port':port,'maxConnections':max_connections}
    db.saveFile('Database/config', config)
else:
    print('Attempting to load server configuration...')
    
    config = db.loadFile('Database/config')
    if config is None:
        print('Failed to load config!')
    else:
        print('Config loaded!')
        print('Starting server...')

        serv = Server(str(config['address']),
                      int(config['port']),
                      int(config['maxConnections']))

        serv.channels['botdom'] = {'owner':'core','desc':'Bots ftw!','title':'this is a title','topic':'this is a topic'} #for now
        serv.channels['datashare'] = {'owner':'core','desc':'Bots ftw!','title':'this is a title','topic':'this is a topic'} #for now
        serv.run()
