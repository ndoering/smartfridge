import configparser


CONFIG_FILE = "config.ini"


class Configuration():
    def __init__(self, config_file=None):
        if config_file is None:
            config_file = CONFIG_FILE

        self.config_file = config_file

        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)


if __name__ == "__main__":
    c = Configuration("../config.ini")
    print(c.config['SLACK']['BotName'])
    print(c.config['SLACK']['SlackChannel'])
    print(c.config['SLACK']['SlackToken'])
