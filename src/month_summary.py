from argparse import ArgumentParser

import capitalone
from category import Category
import common
from config import Config
from rule import Rule
from transaction import Transaction

class MonthlySummary:
    def __init__(self):
        self.categorized_transactions = { category: [] for category in Category }
        self.skipped_transactions = []
        self.credit_transactions = []

    def add_transaction(self, transaction, category):
        self.categorized_transactions[category].append(transaction)

    def skip_transaction(self, transaction):
        self.skipped_transactions.append(transaction)

    def credit_transaction(self, transaction):
        self.credit_transactions.append(transaction)

    def pretty(self):
        # categories
        def category_sum(transactions):
            amounts = [float(transaction.amount) for transaction in transactions]
            return sum(amounts)

        def category_transactions(category, transactions):
            pretty_transactions = common.pretty_transactions(transactions)
            formatted_transactions = '\n\t'.join(pretty_transactions)
            formatted_sum = "{0:.2f}".format(category_sum(transactions))
            return "{}: {}\n\t{}".format(category.name, formatted_sum, formatted_transactions)

        all_category_transactions = '\n'.join([category_transactions(k, v) for k, v in self.categorized_transactions.items()])

        # skipped
        pretty_skipped_transactions = common.pretty_transactions(self.skipped_transactions)
        formatted_skipped_transactions = "skipped:\n\t{}".format('\n\t'.join(pretty_skipped_transactions))

        # credit
        pretty_credit_transactions = common.pretty_transactions(self.credit_transactions)
        formatted_credit_transactions = "unresolved credit:\n\t{}".format('\n\t'.join(pretty_credit_transactions))

        return '\n'.join([all_category_transactions, formatted_skipped_transactions, formatted_credit_transactions])

def maybe_category_from_rule(rules, transaction):
    matching_rules = [rule for rule in rules if rule.description == transaction.description]
    if matching_rules:
        assert(len(matching_rules) == 1, "multiple matching rules for transaction: {}".format(transaction))
        return matching_rules[0]

def summarize(config_filename, capitalone_filename):
    config = Config.from_file(config_filename)
    summary = MonthlySummary()

    transactions = capitalone.parse(capitalone_filename)
    for transaction in transactions:
        print("\n{}".format(transaction.pretty()))
        if transaction.description in config.blacklist:
            print("Blacklisted")
            summary.skip_transaction(transaction)
        elif transaction.amount < 0:
            print("Credit transaction")
            summary.credit_transaction(transaction)
        else:
            matching_rule = maybe_category_from_rule(config.rules, transaction)
            if matching_rule:
                print("Matched rule, category: {}".format(matching_rule.category.name))
                category = matching_rule.category
            else:
                (category, save_choice) = Category.choose()
                if save_choice:
                    config.rules.append(Rule(transaction.description, category))
            summary.add_transaction(transaction, category)

    print(summary.pretty())

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--capitalone', required=True)

    args = parser.parse_args()
    summarize(args.config, args.capitalone)
