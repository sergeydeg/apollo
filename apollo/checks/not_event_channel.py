from discord.ext import commands


class NotEventChannel:

    def __init__(self, bot):
        self.bot = bot

    # Global check to ensure that commands in an event channel
    # are not processed.
    def __call__(self, ctx):
        return not self.bot.cache.event_channel_exists(ctx.channel.id)
