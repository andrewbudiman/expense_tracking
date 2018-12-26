from argparse import ArgumentParser
import csv
import os

import capitalone
from category import Category
import common
from config import Config
from matchers import EqualityMatcher
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

    def to_csv(self, output_dir):
        def write_transactions(writer, transactions):
            for transaction in sorted(transactions, key=lambda t: (t.description, t.date)):
                writer.writerow(transaction.csv_row())

        # categories
        for category, transactions in self.categorized_transactions.items():
            with open(os.path.join(output_dir, "{}.csv".format(category.name)), 'w') as f:
                writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL)
                write_transactions(writer, transactions)

        # unresolved
        with open(os.path.join(output_dir, "unresolved.csv"), 'w') as f:
            writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL)

            # skipped
            writer.writerow(['skipped'])
            write_transactions(writer, self.skipped_transactions)

            # credit
            writer.writerow(['credit'])
            write_transactions(writer, self.credit_transactions)

def maybe_category_from_rule(rules, transaction):
    maybe_categories = [rule.maybe_category(transaction) for rule in rules]
    matching_categories = list(filter(lambda x: x != None, maybe_categories))

    if matching_categories:
        assert len(matching_categories) == 1, "multiple matching rules for transaction: {}".format(transaction)
        return matching_categories[0]

def summarize(config_filename, new_config_filename, capitalone_filename, output_dir):
    config = Config.load_from_file(config_filename)
    summary = MonthlySummary()

    transactions = capitalone.parse(capitalone_filename)
    for transaction in transactions:
        print("\n{}".format(transaction.pretty()))
        
        if next((True for matcher in config.blacklist if matcher.match(transaction)), None):
            print("Blacklisted")
            summary.skip_transaction(transaction)
        elif transaction.amount < 0:
            print("Credit transaction")
            summary.credit_transaction(transaction)
        else:
            matching_category = maybe_category_from_rule(config.rules, transaction)
            if matching_category:
                print("Matched rule, category: {}".format(matching_category.name))
                summary.add_transaction(transaction, matching_category)
            else:
                choice = Category.choose()
                if not choice:
                    summary.skip_transaction(transaction)
                else:
                    (category, save_choice) = choice
                    if save_choice:
                        matcher = EqualityMatcher(transaction.description)
                        config.rules.append(Rule(category, matcher))
                        config.save_to_file(new_config_filename)
                    summary.add_transaction(transaction, category)

    print(summary.pretty())
    if output_dir:
        summary.to_csv(output_dir)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--new-config', required=True)
    parser.add_argument('--capitalone', required=True)
    parser.add_argument('--output-dir')

    args = parser.parse_args()
    summarize(args.config, args.new_config, args.capitalone, args.output_dir)
