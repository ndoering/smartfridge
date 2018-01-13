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

    def compute_message(self, json):
        HIGH_CONF = 0.9
        MEDIUM_CONF = 0.6
        counter = 0
        for concept in json:
            if concept['value'] >= HIGH_CONF:
                print("Looks like " + concept['name'])
                counter += 1
            elif concept['value'] >= MEDIUM_CONF:
                print("Might be " + concept['name'])
                counter += 1

        if counter == 0:
            print("I am unsure about the fridge's content.")

    def speak(self):
        message = get_message("neutral")

        sc.send_message(self.slackClient,
                        self.configuration["SLACK"]["BotName"],
                        self.configuration["SLACK"]["SlackChannel"],
                        message)
