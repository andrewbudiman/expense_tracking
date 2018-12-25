from argparse import ArgumentParser
import json

from rule import Rule

class Config:

    def __init__(self, config_map):
        self.blacklist = config_map['blacklist']
        self.rules = [Rule(rule['description'], rule['category']) for rule in config_map['rules']]

    @staticmethod
    def from_file(filename):
        with open(filename, 'r') as f:
            return Config(json.loads(f.read()))

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('file', help='config file')

    args = parser.parse_args()
    Config.from_file(args.file)
