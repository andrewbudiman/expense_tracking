from argparse import ArgumentParser
import json

import matchers
from rule import Rule

class Config:
    def __init__(self, config_map):
        self.blacklist = [matchers.from_raw(m) for m in config_map['blacklist']]
        self.rules = [Rule.from_raw(rule) for rule in config_map['rules']]

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r') as f:
            return Config(json.loads(f.read()))

    def save_to_file(self, filename):
        config_map = {
                'blacklist': [matcher.to_raw() for matcher in self.blacklist],
                'rules': [rule.to_raw() for rule in self.rules]
        }

        with open(filename, 'w') as f:
            f.write(json.dumps(config_map, indent=2, sort_keys=True) + "\n")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('file', help='config file')

    args = parser.parse_args()
    Config.load_from_file(args.file)
