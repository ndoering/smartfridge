from slackclient import SlackClient

TOKEN = 'xoxp-267167456709-268110163879-280860661282-a4fd156159fbab0ba6d2b7e3b24b3e1d'
BOT_CHANNEL='C8650A1C1'
BOT_NAME='FridgeBot'


slack_client = SlackClient(TOKEN)

def list_channels():
    '''Returns a list of all channels within the team'''
    channels_call = slack_client.api_call("channels.list")
    if channels_call['ok']:
        return channels_call['channels']
    return None


def channel_info(channel_id):
    '''Get the info for a given channel'''
    channel_info = slack_client.api_call("channels.info", channel=channel_id)
    if channel_info:
        return channel_info['channel']
    return None

def send_message(channel_id, message):
    '''Sends a message to a given channel.'''
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username=BOT_NAME,
        icon_emoji=':robot_face:'
    )

if __name__ == '__main__':
    send_message(BOT_CHANNEL, "This is the fridge speaking: Hello, dear world")