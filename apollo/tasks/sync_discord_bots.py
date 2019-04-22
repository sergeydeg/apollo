from discord.ext import tasks, commands


class SyncDiscordBots(commands.Cog):

    def __init__(self, dbl_client):
        self.dbl_client = dbl_client
        self.update_server_count.start()


    @tasks.loop(seconds=60)
    async def update_server_count(self):
        await self.dbl_client.post_server_count()
