from collections import namedtuple
from dataclasses import dataclass

class Transaction:

    def __init__(self, date: str, description: str, debit: str, credit: str):
        self.date = date
        self.description = description

        # calculate a raw amount
        parsed_debit = float(debit) if debit else 0
        parsed_credit = float(credit) if credit else 0
        assert parsed_debit or parsed_credit
        self.amount = parsed_debit - parsed_credit

    def pretty(self):
        return "{} {} {}".format(
                self.date,
                self.description,
                "{0:.2f}".format(self.amount)
        )
