class Command:
    def __init__(self, body):
        self.channel_id = body['channel_id']
        self.channel_name = body['channel_name']
        self.user_id = body['user_id']
        self.user_name = body['user_name']
        self.command = body['command']
        self.text = body['text']
        self.response_url = body['response_url']
        self.trigger_id = body['trigger_id']