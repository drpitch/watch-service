import json
import sys

import matcher
import notifier
import mailer

class WatchService(object):
    """
    Main service responsible for calling notifiers when input data matches any
    defined rule.
    """
    def __init__(self, config):
        self.config = config

    def run(self, inputstream):
        if isinstance(inputstream, str):
            self.__watch(inputstream)
        else:
            for line in inputstream:
                self.__watch(line)

    def __watch(self, line):
        for m in self.config.matchers:
            if m.matches(line):
                self.__notify(line)

    def __notify(self, line):
        for n in self.config.notifiers:
            n.notify(line)


class Configuration(object):
    """
    Load JSON data from a settings file and setup matchers and notifiers.

    This is how a settings file would look like:
    {
        "matchers": [
            {
                "type": "Sentence",
                "text": "I see trees of green"
            },
            {
                "type": "RegExp",
                "pattern": "(hello|go(o)+dbye)"
            }
        ],

        "notifiers": [
            {
                "type": "Console"
            },
            {
                "type": "Mail",
                "options": {
                    "provider": "SMTP",
                    "host": "localhost",
                    "port": "25"
                    "from": "me@mail.com",
                    "to": "you@mail.com",
                    "subject": "The Subject"
                }
            }
        ]
    }

    "host" and "port" option keys in Mail notifier are not required.
    Default values for "host" and "port" are "localhost" and "25", respectively.
    """
    class MatcherFactory(object):
        """
        Factory that handles object creation of matchers.
        """
        def sentence(parameters):
            try:
                text = parameters["text"]
            except KeyError:
                raise KeyError("'text' key required but not specified in Sentence matcher.")

            return matcher.SentenceMatcher(text)

        def regexp(parameters):
            try:
                pattern = parameters["pattern"]
            except KeyError:
                raise KeyError("'pattern' key required but not specified in Patern matcher.")

            return matcher.RegExpMatcher(pattern)


    class NotifierFactory(object):
        """
        Factory that handles object creation of notifiers.
        """
        def console(parameters):
            return notifier.ConsoleNotifier()

        def mail(parameters):
            if "options" not in parameters:
                raise KeyError("'options' key required but not specified in Mail Notifier.")

            for option in ["provider", "from", "to", "subject"]:
                if option not in parameters["options"]:
                    raise KeyError("'{0}' key required but not specified in Mail Notifier.".format(option))

            if parameters["options"]["provider"] == "SMTP":
                host = parameters["options"].get("host", "localhost")
                port = parameters["options"].get("port", "25")
                provider = mailer.SMTP(host, port)
            elif parameters["options"]["provider"] == "Dumper":
                provider = mailer.Dumper()
            else:
                raise ValueError("Invalid provider value {0} in Mail Notifier".format(parameters["options"]["provider"]))

            subject = parameters["options"]["subject"]
            from_address = parameters["options"]["from"]
            to_address = parameters["options"]["to"]

            return notifier.MailNotifier(provider, subject, from_address, to_address)

    def __init__(self, filename):
        with open(filename) as data_file:
            config = json.load(data_file)

        self.__set_matchers(config["matchers"])
        self.__set_notifiers(config["notifiers"])

    def __set_matchers(self, matchers):
        types = {
            "Sentence" : self.MatcherFactory.sentence,
            "RegExp"   : self.MatcherFactory.regexp,
        }

        self.matchers = []

        for matcher in matchers:
            try:
                callable_ = types[matcher["type"]]
            except:
                raise ValueError("Invalid matcher value: {0}.".format(matcher["type"]))
            else:
                self.matchers.append(callable_(matcher))

    def __set_notifiers(self, notifiers):
        types = {
            "Console" : self.NotifierFactory.console,
            "Mail"   : self.NotifierFactory.mail,
        }

        self.notifiers = []

        for notifier in notifiers:
            try:
                callable_ = types[notifier["type"]]
            except:
                raise ValueError("Invalid notifier value: {0}.".format(notifier["type"]))
            else:
                self.notifiers.append(callable_(notifier))


if __name__ == "__main__":
    w = WatchService(Configuration("settings.json"))

    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            w.run(f)
    else:
        w.run(sys.stdin)
