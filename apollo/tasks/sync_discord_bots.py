import asyncio

from discord.ext import commands


class SyncDiscordBots(commands.Cog):
    def __init__(self, bot, dbl_client):
        self.bot = bot
        self.dbl_client = dbl_client
        self.bot.loop.create_task(self.update_server_count())

    async def update_server_count(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            await self.dbl_client.post_server_count()
            await asyncio.sleep(1800)
