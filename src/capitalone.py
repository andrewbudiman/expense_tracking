from argparse import ArgumentParser
import csv

from transaction import Transaction

def transaction_from_fields(fields):
    print(fields)
    return Transaction(
            date=fields[0],
            description=fields[3],
            debit=fields[5],
            credit=fields[6]
    )

def parse(filename):
    with open(filename, 'r') as f:
        return [transaction_from_fields(fields) for fields in csv.reader(f, quotechar='"', quoting=csv.QUOTE_ALL)]

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('file', help='csv file')

    args = parser.parse_args()
    parse(args.file)
