import configparser


CONFIG_FILE = "config.ini"


configreader = configparser.ConfigParser()


def read_config():
    configreader.read(CONFIG_FILE)


def write_config():
    with open(CONFIG_FILE, 'w') as configfile:
        configreader.write(configfile)


class Configuration():
    def __init__(self):
        read_config()
        self.config = configreader


if __name__ == "__main__":
    read_config()
    print(configreader['SLACK']['BotName'])
    print(configreader['SLACK']['SlackChannel'])
    print(configreader['SLACK']['SlackToken'])
