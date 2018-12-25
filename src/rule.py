from category import Category
import matchers

class Rule:
    def __init__(self, category, matcher):
        self.category = category
        self.matcher = matcher

    @staticmethod
    def from_raw(raw):
        category = Category(raw['category'])
        matcher = matchers.from_raw(raw['matcher'])
        return Rule(category, matcher)

    def to_raw(self):
        return {
                'category': self.category.value,
                'matcher': self.matcher.to_raw()
        }

    def maybe_category(self, transaction):
        if self.matcher.match(transaction):
            return self.category
