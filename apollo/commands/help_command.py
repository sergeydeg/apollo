from discord.ext import commands

from apollo.embeds import HelpEmbed


class HelpCommand(commands.Cog):
    def __init__(self, bot, help_embed):
        self.bot = bot
        self.help_embed = help_embed

        # Remove default help command
        self.bot.remove_command("help")

    @commands.command(hidden=True)
    async def help(self, ctx):
        help_embed = self.help_embed.call(ctx.prefix, self.bot.commands)
        await ctx.send(embed=help_embed)
