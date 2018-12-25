from argparse import ArgumentParser

import capitalone
from category import Category
import common
from config import parse_config
from transaction import Transaction

class MonthlySummary:
    def __init__(self):
        self.categorized_transactions = { category: [] for category in Category }
        self.skipped_transactions = []

    def add_transaction(self, transaction, category):
        self.categorized_transactions[category].append(transaction)

    def skip_transaction(self, transaction):
        self.skipped_transactions.append(transaction)

    def pretty(self):
        def category_sum(transactions):
            amounts = [float(transaction.debit) for transaction in transactions]
            return sum(amounts)

        def category_transactions(category, transactions):
            pretty_transactions = common.pretty_transactions(transactions)
            formatted_transactions = '\n\t'.join(pretty_transactions)
            formatted_sum = "{0:.2f}".format(category_sum(transactions))
            return "{}: {}\n\t{}".format(category.name, formatted_sum, formatted_transactions)

        all_category_transactions = '\n'.join([category_transactions(k, v) for k, v in self.categorized_transactions.items()])

        pretty_skipped_transactions = common.pretty_transactions(self.skipped_transactions)
        formatted_skipped_transactions = "\nskipped:\n\t{}".format('\n\t'.join(pretty_skipped_transactions))

        return all_category_transactions + formatted_skipped_transactions

def summarize(config_filename, capitalone_filename):
    config = parse_config(config_filename)
    summary = MonthlySummary()

    transactions = capitalone.parse(capitalone_filename)
    for transaction in transactions[:5]:
        if transaction.description in config['blacklist']:
            summary.skip_transaction(transaction)
        else:
            print("\n{}".format(transaction.pretty()))
            category = Category.choose()
            summary.add_transaction(transaction, category)

    print(summary.pretty())

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--capitalone', required=True)

    args = parser.parse_args()
    summarize(args.config, args.capitalone)
