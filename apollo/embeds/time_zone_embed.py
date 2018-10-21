import discord

from apollo.constants import EMBED_COLOR
from apollo.time_zones import ISO_TIME_ZONES
from apollo.translate import t


class TimeZoneEmbed:

    def __init__(self):
        pass


    def call(self):
        embed = discord.Embed()
        embed.color = EMBED_COLOR
        embed.title = t("time_zone.title")

        embed.description = ""
        for i, time_zone in enumerate(ISO_TIME_ZONES, 1):
            embed.description += "**{}** {}\n".format(i, time_zone)

        return embed

