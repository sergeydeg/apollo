from discord.ext import commands


class Ping:

    def __init__(self, bot, session_scope):
        self.bot = bot
        self.session_scope = session_scope


    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")
