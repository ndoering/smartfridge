import slack_connector as sc
import configuration_management as conf


if __name__ == "__main__":
    c = conf.Configuration()
    bot = sc.Slackbot(c)
    bot.speak()
