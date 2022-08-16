from loguru import logger
from slack_bolt.app.async_app import AsyncApp

from slackbot.command import Command


class SubApp:
    def __init__(self) -> None:
        self.actions = []
        self.events = []
        self.views = []
        self.commands = []

    def action(self, *args, **kwargs):
        def __call__(func):
            self.actions.append((args, kwargs, func))
            return func

        return __call__

    def command(self, *args, **kwargs):
        def __call__(func):
            async def __func__(ack, body):
                command = Command(body)
                logger.trace(
                    f"Acknowledging command {command.command}, triggered by {command.user_name} ({command.user_id}) in "
                    f"{command.channel_name} ({command.channel_id})")
                await ack()
                return await func(command)
            self.commands.append((args, kwargs, __func__))
            return func

        return __call__

    def event(self, *args, **kwargs):
        def __call__(func):
            self.events.append((args, kwargs, func))
            return func

        return __call__

    def view(self, *args, **kwargs):
        def __call__(func):
            self.views.append((args, kwargs, func))
            return func

        return __call__

    def register_to(self, app: AsyncApp):
        for args, kwargs, func in self.actions:
            app.action(*args, **kwargs)(func)
        for args, kwargs, func in self.commands:
            app.command(*args, **kwargs)(func)
        for args, kwargs, func in self.events:
            app.event(*args, **kwargs)(func)
        for args, kwargs, func in self.views:
            app.view(*args, **kwargs)(func)
