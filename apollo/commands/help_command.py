from discord.ext import commands

from apollo.embeds import HelpEmbed


class HelpCommand:

    def __init__(self, bot):
        self.bot = bot

        # Remove default help command
        self.bot.remove_command("help")


    @commands.command(hidden=True)
    async def help(self, ctx):
        help_embed = HelpEmbed(ctx.prefix, self.bot.commands).call()
        await ctx.send(embed=help_embed)
