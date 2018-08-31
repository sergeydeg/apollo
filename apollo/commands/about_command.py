from discord.ext import commands

from apollo.embeds import AboutEmbed


class AboutCommand:

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def about(self, ctx):
        session = self.bot.Session()
        about_embed = AboutEmbed(self.bot, session).call()
        await ctx.send(embed=about_embed)
