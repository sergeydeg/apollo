import asyncio

from discord.ext import commands

from apollo.translate import t


class OnCommandError:

    def __init__(self, bot):
        self.bot = bot


    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            return
        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.send(t("error.private_message"))
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send(t("error.missing_permissions"))
        elif isinstance(error, commands.CheckFailure):
            return
        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, asyncio.TimeoutError):
                return await ctx.author.send(t("error.timeout"))
            else:
                raise error
        else:
            raise error
