from slack_bolt.app.async_app import AsyncApp


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
            self.commands.append((args, kwargs, func))
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
