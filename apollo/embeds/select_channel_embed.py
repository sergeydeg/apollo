import discord

from apollo import emojis as emoji
from apollo.constants import EMBED_COLOR
from apollo.translate import t


class SelectChannelEmbed:
    def __init__(self, channels):
        self.channels = channels

    def call(self):
        embed = discord.Embed()
        embed.color = EMBED_COLOR
        embed.title = t("select_channel.title")
        embed.description = self._channel_list()
        return embed

    def _channel_list(self):
        desc = ""
        for i, channel in enumerate(self.channels):
            desc += f"{emoji.NUMBERS[i]}: {channel.name}\n"
        return desc
