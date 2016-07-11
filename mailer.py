import smtplib
from email.mime.text import MIMEText

class Dumper(object):
    '''
    Dump emails to standard output.
    '''
    def send(self, subject, from_address, to_address, content):
        print("New message:")
        print("\t   From: {0}".format(from_address))
        print("\t     To: {0}".format(to_address))
        print("\tSubject: {0}".format(subject))
        print("\tContent: {0}".format(content))


class SMTP(object):
    '''
    Send emails using a SMTP server.
    '''
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send(self, subject, from_address, to_address, content):
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = to_address

        with smtplib.SMTP(self.host, self.port) as smtp:
            server.send_message(msg)
