import asyncio

from discord.ext import commands


class OnCommandError:

    def __init__(self, bot):
        self.bot = bot


    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            return
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("You can't use that command in a private message.")
            return
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have permission to do that.")
            return
        elif isinstance(error.original, asyncio.TimeoutError):
            await ctx.author.send("I'm not sure where you went. We can try this again later.")
            return

        raise error
