class MailNotifier(object):
    '''
    Notifier that sends information by email.
    '''
    def __init__(self, mailer_service, subject, from_address, to_address):
        self.mailer_service = mailer_service
        self.subject = subject
        self.from_address = from_address
        self.to_address = to_address

    def notify(self, line):
        self.mailer_service.send(self.subject, self.from_address, self.to_address, line)


class ConsoleNotifier(object):
    '''
    Notifier that prints information to standard output.
    '''
    def notify(self, line):
        print(line)
