import imaplib
import ConfigParser
import os

def open_connection(verbose=False):
    config = ConfigParser.ConfigParser()
    config.read([os.path.expanduser('cred.cfg')])

    hostname = config.get('server', 'hostname')
    username = config.get('server', 'username')
    password = config.get('server', 'password')

    if verbose: print('Connecting to ', hostname)
    connection = imaplib.IMAP4_SSL(hostname)
    if verbose: print('Logging in as ', username)
    connection.login(username, password)
    return connection
if __name__=='__main__':
    c = open_connection(verbose=True)
    try:
        typ, data = c.list()
<<<<<<< HEAD
        print('Response Code: ', typ)
        print('Response: ', data)
=======
        print('Response Code: ',typ)
        print('Response: ')
        pprint(data)
>>>>>>> 6aeeac524f0b7f62ab55e5b9549b6d54007692c2
    finally:
        c.logout()
