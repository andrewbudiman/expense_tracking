from argparse import ArgumentParser

import capitalone
from category import Category
from transaction import Transaction

class MonthlySummary:
    def __init__(self):
        self.categorized_transactions = { category: [] for category in Category }

    def add_transaction(self, transaction, category):
        self.categorized_transactions[category].append(transaction)

    def pretty(self):
        def category_sum(transactions):
            amounts = [float(transaction.debit) for transaction in transactions]
            return sum(amounts)

        def category_transactions(category, transactions):
            pretty_transactions = [t.pretty() for t in transactions]
            formatted_transactions = '\n\t'.join(pretty_transactions)
            formatted_sum = "{0:.2f}".format(category_sum(transactions))
            return "{}: {}\n\t{}".format(category.name, formatted_sum, formatted_transactions)

        return '\n'.join([category_transactions(k, v) for k, v in self.categorized_transactions.items()])

def summarize(capitalone_filename):
    summary = MonthlySummary()

    transactions = capitalone.parse(capitalone_filename)
    for transaction in transactions[:2]:
        print("\n{}".format(transaction.pretty()))
        category = Category.choose()
        summary.add_transaction(transaction, category)

    print(summary.pretty())

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('capitalone')

    args = parser.parse_args()
    summarize(args.capitalone)
