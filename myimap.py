import imaplib
import ConfigParser
import os

def open_connection(verbose=False):
    config = ConfigParser.ConfigParser()
    config.read([os.path.expanduser('cred.txt')])

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
        print(c)
    finally:
        c.logout()
