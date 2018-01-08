import imaplib
import configparser
import os
import email
import datetime
import codecs

now = datetime.datetime.now()

def open_connection(verbose=False):
    config = configparser.ConfigParser()
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
    f = codecs.open(now.strftime("%Y%m%d") + '.csv', 'a', 'utf-8')
    c = open_connection(verbose=True)
    try:
        c.list()
        c.select(mailbox='INBOX',readonly=True)
        #result, emdata = c.uid('search', None, "ALL")
        result, emdata = c.sort('DATE', 'UTF-8', 'ALL')
        for x in emdata[0].split():
            # print('Processing: ',x)
            ret, data = c.fetch(x,'(RFC822)')
            if ret != 'OK':
                print('Error with message: ',x)
            msg = email.message_from_bytes(data[0][1])
            # print(str(msg))
            try:
                fromhdr = email.header.make_header(email.header.decode_header(msg['From']))
                fromstr = str(fromhdr).replace('\n', ' ').replace('\r', ' ').replace('|','\|').replace('"','\\"')
                subjhdr = email.header.make_header(email.header.decode_header(msg['Subject']))
                subjstr = str(subjhdr).replace('\n', ' ').replace('\r', ' ').replace('|','\|').replace('"','\\"')
                date_tuple = email.utils.parsedate_tz(msg['Date'])
                if date_tuple:
                    local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                # print ("Local Date:", local_date.strftime("%a, %d %b %Y %H:%M:%S"))
                # print('%s|%s|%s' % (local_date.strftime("%Y-%m-%d %H:%M:%S"),fromstr, subjstr))
                f.write('%s|%s|%s|%s\n' % (x,local_date.strftime("%Y-%m-%d %H:%M:%S"),fromstr, subjstr))
            except:
                print("Ignoring: ",str(msg))
    finally:
        c.logout()
        f.close()
