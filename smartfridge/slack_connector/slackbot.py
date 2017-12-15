from slackclient import SlackClient
import slack_connector as sc
import random


messages = {
    "neutral": [
        "This is the fridge. Its so cool here.",
        "I am the fridge, cool as always",
        "This is the fridge speaking, ice to meet you."
    ],
    "lonely": [
        "Is anybody there? Its so cold and dark.",
        "Is there nobody looking for food... or me?"
    ]
}


def get_message(type):
    message_list = messages[type]
    rnd = random.randrange(len(message_list))

    return message_list[rnd]


class Slackbot():
    def __init__(self, configuration):
        self.configuration = configuration.config
        self.slackClient = SlackClient(self.configuration["SLACK"]["SlackToken"])

    def speak(self):
        message = get_message("neutral")

        sc.send_message(self.slackClient,
                        self.configuration["SLACK"]["BotName"],
                        self.configuration["SLACK"]["SlackChannel"],
                        message)
