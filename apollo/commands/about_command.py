from discord.ext import commands

from apollo.embeds import AboutEmbed


class AboutCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def about(self, ctx):
        """Display information about the bot"""
        session = self.bot.Session()
        about_embed = AboutEmbed(self.bot, session).call()
        await ctx.send(embed=about_embed)
