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
        embed.description = t("time_zone.footer").format(self.INVITE)

        time_zone_index = 1

        for region, time_zones in ISO_TIME_ZONES.items():
            time_zone_list = ""

            for time_zone in time_zones:
                time_zone_name = t("time_zones.{}".format(time_zone.lower()))
                time_zone_list += "**{}** {}\n".format(time_zone_index, time_zone_name)
                time_zone_index += 1

            embed.add_field(name=t(region), value=time_zone_list)

        return embed
