import imaplib
import ConfigParser
import os
import email

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
        c.select(mailbox='INBOX',readonly=True)
        result, emdata = c.uid('search', None, "ALL")
        for x in emdata[0].split():
            ret, data = c.fetch(x,'(RFC822)')
            if ret != 'OK':
                print('Error with message: ',x)
            msg = email.message_from_string(data[0][1])
            hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
            subject = str(hdr)
            print 'Message %s: %s' % (x, subject)
            break
    finally:
        c.logout()
