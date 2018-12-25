from category import Category

class Rule:

    def __init__(self, description, category_str):
        self.description = description
        self.category = Category(category_str)
