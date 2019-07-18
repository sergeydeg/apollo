import discord

from apollo.constants import EMBED_COLOR
from apollo.translate import t


class StartTimeEmbed:
    def __init__(self):
        pass

    def call(self, event_title, formatted_start_time):
        embed = discord.Embed(title=event_title)
        embed.color = EMBED_COLOR
        embed.description = t("event.local_start_time").format(formatted_start_time)
        return embed

