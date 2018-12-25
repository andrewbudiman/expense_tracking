from argparse import ArgumentParser
import json

from rule import Rule

class Config:

    def __init__(self, config_map):
        self.blacklist = config_map['blacklist']
        self.rules = [Rule(rule['description'], rule['category']) for rule in config_map['rules']]

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r') as f:
            return Config(json.loads(f.read()))

    def save_to_file(self, filename):
        config_map = {
                'blacklist': self.blacklist,
                'rules': [
                    {
                        'description': rule.description,
                        'category': rule.category.value
                    }
                    for rule in self.rules
                ]
        }

        with open(filename, 'w') as f:
            f.write(json.dumps(config_map, indent=2, sort_keys=True) + "\n")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('file', help='config file')

    args = parser.parse_args()
    Config.load_from_file(args.file)
