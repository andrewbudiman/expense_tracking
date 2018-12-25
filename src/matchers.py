class EqualityMatcher:
    def __init__(self, text):
        self.description = text

    @staticmethod
    def matcher_type():
        return "eq"

    def match(self, transaction):
        return transaction.description == self.description

    def to_raw(self):
        return {
                'text': self.description,
                'type': EqualityMatcher.matcher_type()
        }

class PrefixMatcher:
    def __init__(self, text):
        self.prefix = text

    @staticmethod
    def matcher_type():
        return "prefix"

    def match(self, transaction):
        return transaction.description.startswith(self.prefix)

    def to_raw(self):
        return {
                'text': self.prefix,
                'type': PrefixMatcher.matcher_type()
        }

def from_raw(raw):
    matcher_type = raw['type']
    text = raw['text']

    if matcher_type == EqualityMatcher.matcher_type():
        return EqualityMatcher(text)
    elif matcher_type == PrefixMatcher.matcher_type():
        return PrefixMatcher(text)
    else:
        raise Exception("Unknown matcher type: {}".format(matcher_type))
