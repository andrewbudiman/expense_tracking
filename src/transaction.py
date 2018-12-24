from collections import namedtuple
from dataclasses import dataclass

class Transaction:

    def __init__(self, date: str, description: str, debit: str, credit: str):
        self.date = date
        self.description = description
        self.debit = float(debit) if debit else 0
        self.credit = float(credit) if credit else 0
        # xcxc - what to do with credit?

    def pretty(self):
        return "{} {} {}".format(
                self.date,
                self.description,
                self.debit
        )
