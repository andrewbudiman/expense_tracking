from enum import Enum
import sys

class Category(Enum):
    Need = 1
    Okay = 2
    Food = 3
    Coffee = 4
    Fun = 5

    @staticmethod
    def choose():
        print('Choose a category')
        for category in Category:
            print("\t{}: {}".format(category.value, category.name))
    
        choice = sys.stdin.readline()
        try:
            return Category(int(choice.strip()))
        except ValueError:
            print('Invalid input, try again.')
            return get_category()
