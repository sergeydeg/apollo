import discord

from apollo.constants import EMBED_COLOR
from apollo.time_zones import ISO_TIME_ZONES
from apollo.translate import t


class TimeZoneEmbed:
    INVITE = "https://discord.gg/PQXA2ys"

    def __init__(self):
        pass


    def call(self):
        embed = discord.Embed()
        embed.color = EMBED_COLOR
        embed.title = t("time_zone.title")

        embed.description = ""
        for i, iso_time_zone in enumerate(ISO_TIME_ZONES, 1):
            time_zone_name = t("time_zones.{}".format(iso_time_zone.lower()))
            embed.description += "**{}** {}\n".format(i, time_zone_name)
        embed.description += "\n"
        embed.description += t("time_zone.footer").format(self.INVITE)

        return embed

