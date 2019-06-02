from discord.ext import commands

from apollo.queries import event_channel_exists


class NotEventChannel:

    def __init__(self, bot):
        self.bot = bot

    # Global check to ensure that commands in an event channel
    # are not processed.
    def __call__(self, ctx):
        with self.bot.scoped_session() as session:
            if event_channel_exists(session, ctx.channel.id):
                return False
            else:
                return True
