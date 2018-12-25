from enum import Enum
import sys

class Category(Enum):
    # Keep a stable ordering please
    Need = 'Need'
    Okay = 'Okay'
    Food = 'Food'
    Coffee = 'Coffee'
    Fun = 'Fun'

    @staticmethod
    def choose():
        assert len(Category) < 10, "Code assumes there are fewer than 10 cagegories"
        print('Choose a category (10, 20, etc to choose and create a rule)')
        print('\t0: Skip')
        for idx, category in enumerate(list(Category)):
            print("\t{}: {}".format(1+idx, category.name))
    
        try:
            choice = int(sys.stdin.readline().strip())
            save_choice = False

            if not choice:
                return None

            if choice >= 10:
                save_choice = True
                choice = int(choice / 10)

            chosen_category = list(Category)[choice - 1]
            return (chosen_category, save_choice)
        except ValueError:
            print('Invalid input, try again.')
            return Category.choose()
