import argparse as ap

class CliParser:
    def __init__(self):
        self.parser = ap.ArgumentParser(prefix_chars='--')
        self.parser.add_argument('--config', help='Specify the config file to be used')

        self.args = self.parser.parse_args()

if __name__ == "__main__":
    parser = CliParser()

    print(parser.args.config)