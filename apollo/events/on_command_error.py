import os

import bugsnag


class OnCommandError:

    def __init__(self, bot):
        self.bot = bot


    async def on_command_error(self, ctx, exception):
        if os.getenv('ENV') == 'production':
            bugsnag.notify(exception)
        raise exception
