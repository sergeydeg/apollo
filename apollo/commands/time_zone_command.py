from discord.ext import commands

from apollo.queries import find_or_create_user
from apollo.translate import t


class TimeZoneCommand(commands.Cog):
    def __init__(self, bot, time_zone_embed, time_zone_input):
        self.bot = bot
        self.time_zone_embed = time_zone_embed
        self.time_zone_input = time_zone_input

    @commands.command()
    async def timezone(self, ctx):
        """Set your local time zone"""
        await ctx.send(embed=self.time_zone_embed.call())
        time_zone = await self.time_zone_input.call(ctx.author, ctx.channel)

        with self.bot.scoped_session() as session:
            user = find_or_create_user(session, ctx.author.id)
            user.time_zone = time_zone
            session.add(user)

        humanized_time_zone = t("time_zones.{}".format(time_zone.lower()))
        await ctx.send(t("time_zone.updated").format(humanized_time_zone))
