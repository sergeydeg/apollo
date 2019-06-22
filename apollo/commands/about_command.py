from discord.ext import commands

from apollo.embeds import AboutEmbed
from apollo.queries import total_user_count
from apollo.queries import total_event_count


class AboutCommand(commands.Cog):
    def __init__(self, bot, about_embed):
        self.bot = bot
        self.about_embed = about_embed

    @commands.command()
    async def about(self, ctx):
        """Display information about the bot"""
        with self.bot.scoped_session() as session:
            user_count = total_user_count(session)
            event_count = total_event_count(session)

        about_embed = self.about_embed.call(user_count, event_count, len(self.bot.guilds))
        await ctx.send(embed=about_embed)
