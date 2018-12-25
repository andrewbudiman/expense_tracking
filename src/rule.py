from category import Category

class Rule:

    def __init__(self, description, category_int):
        self.description = description
        self.category = Category(category_int)
