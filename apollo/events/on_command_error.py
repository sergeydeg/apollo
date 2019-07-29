import asyncio

from discord.errors import Forbidden
from discord.ext import commands

from apollo.translate import t


class OnCommandError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            pass
        elif isinstance(error, commands.BadArgument):
            await ctx.send(error)
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(t("error.private_message"))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(t("error.missing_permissions"))
        elif isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, asyncio.TimeoutError):
                await ctx.channel.send(t("error.timeout"))
            elif isinstance(error.original, Forbidden):
                if error.original.text == "Cannot send messages to this user":
                    await ctx.send(t("error.cannot_private_message"))
                else:
                    raise error
            else:
                raise error
        else:
            raise error
