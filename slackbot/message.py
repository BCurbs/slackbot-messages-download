from decimal import Decimal


class Message:
    def __init__(self, body):
        self.ts = Decimal(body['ts'])
        self.id = body['ts']
        self.type = body['type']
        self.user = body['user']
        self.text = body['text']
