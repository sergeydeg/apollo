class OnCommandError:

    def __init__(self, bot):
        self.bot = bot


    async def on_command_error(self, ctx, exception):
        raise exception
