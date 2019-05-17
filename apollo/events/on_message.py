from discord.errors import Forbidden
from discord.ext import commands

from apollo.translate import t


class OnMessage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        # Delete user messages sent to event channels and notify them
        # as to why this is being done.
        #
        # Many users do not initially understand the intention behind
        # event channels, and end up using them as regular channels, only
        # to have a rude awakening when the channel is cleared.
        if not self.bot.cache.event_channel_exists(message.channel.id):
            return

        if self.bot.cache.event_exists(message.id):
            return

        if message.author.id == self.bot.user.id:
            return

        await message.delete()
        try:
            await message.author.send(
                t("notify.message_deleted").format(message.channel.mention)
            )
        except Forbidden:
            pass
