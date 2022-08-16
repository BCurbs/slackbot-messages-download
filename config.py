import json
import os


class Config:
    config_file = 'config.json'
    config = {
        'slack_app_token': 'app token here',
        'slack_bot_token': 'bot token here',
        'db_url': 'database url here',
        'log_level': "info"
    }

    def __init__(self):
        self.load_from_file()
        self.update_file()
        self.slack_app_token: str = self.config['slack_app_token']
        self.slack_bot_token: str = self.config['slack_bot_token']
        self.db_url: str = self.config['db_url']
        self.log_level: str = self.config['log_level'].upper()
        self.check_values()

    def update_file(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent='\t')

    def load_from_file(self):
        if os.path.isfile(self.config_file):
            with open(self.config_file) as f:
                self.config.update(json.load(f))
        else:
            self.update_file()
            exit(f"Config file created at {self.config_file}")

    def check_values(self):
        if not self.slack_bot_token.startswith('xoxb-'):
            exit('Your slack bot token is invalid, it must start with xoxb-')
        if not self.slack_app_token.startswith('xapp-'):
            exit('Your slack app token is invalid, it must start with xapp-')
        if not self.log_level.lower() in ['trace', 'debug', 'info', 'success', 'warning', 'error', 'critical']:
            exit("You must have a valid log level. ")
