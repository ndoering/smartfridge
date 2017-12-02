import configparser

CONFIG_FILE = "config.ini"

config = configparser.ConfigParser()

def read_config():
    config.read(CONFIG_FILE)

def write_config():
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    read_config()
    print(config['SLACK']['BotName'])
    print(config['SLACK']['SlackChannel'])
    print(config['SLACK']['SlackToken'])
