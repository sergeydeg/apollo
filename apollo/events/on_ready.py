from discord.ext import commands


class OnReady(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name} - Ready")

        # Load items into cache
        self.bot.cache.load_prefixes()
        self.bot.cache.load_event_channel_ids()
        self.bot.cache.load_event_message_ids()
