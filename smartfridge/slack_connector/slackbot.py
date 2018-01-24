from slackclient import SlackClient
import slack_connector as sc
import random


messages = {
    "banana_bad": [
        "Attention! There seems to be a bad banana in your fridge.",
        "Oh no, take a look at the banana in your fridge!",
        "The banana in your fridge doesn't look yummy...",
        "Aren't bananas supposed to be yellow?"
    ]
}


def get_message(message_type):
    message_list = messages[message_type]
    rnd = random.randrange(len(message_list))

    return message_list[rnd]


class Slackbot():
    def __init__(self, configuration):
        self.configuration = configuration.config
        self.slackClient = SlackClient(self.configuration["SLACK"]["SlackToken"])

    def compute_message(self, json):
        CONFIDENCE = 0.6
        for concept in json:
            try:
                if messages[concept['name']]:
                    if concept['value'] >= CONFIDENCE:
                        self.speak(concept['name'])
            except:
                continue




    def speak(self, message_type):
        message = get_message(message_type)
        sc.send_message(self.slackClient,
                        self.configuration["SLACK"]["BotName"],
                        self.configuration["SLACK"]["SlackChannel"],
                        message)
