from argparse import ArgumentParser
import json

def parse_config(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('file', help='config file')

    args = parser.parse_args()
    parse(args.file)
