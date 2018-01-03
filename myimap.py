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
        c.list()
        c.select('inbox')
        result, data = c.uid('search', None, "ALL")
        i = len(data[0].split())
        print('Response: ', i)
    finally:
        c.logout()
