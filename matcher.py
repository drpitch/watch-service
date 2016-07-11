import re

class RegExpMatcher(object):
    '''
    Match input lines with a regular expression.
    '''
    def __init__(self, pattern):
        self.regexp = re.compile(pattern)

    def matches(self, line):
        return self.regexp.search(line) != None


class SentenceMatcher(RegExpMatcher):
    '''
    Match input lines with a sentence.
    '''
    def __init__(self, sentence):
        super().__init__(r'\b{0}\b'.format(re.escape(sentence)))
