import discord

from apollo.constants import EMBED_COLOR


class SelectionEmbed:
    def call(self, message_dict, title, footer):
        """
        Takes a dictionary and enumerates it so that the user can select one
        :param message_dict: list or dict
        :param title: str, title, if None, will say generic message
        :param footer: str, usually used for cancellation message
        :return: discord Embed
        """
        embed = discord.Embed(title=title)
        embed.colour = EMBED_COLOR
        embed.set_footer(text=footer)
        self._handle_dict_fields(embed, message_dict)
        return embed

    def _handle_dict_fields(self, embed, message_dict):
        """Handle fields for a dict"""
        for counter, data in enumerate(message_dict.items()):
            key, value = data
            name = f"**{counter + 1}** {key}"
            embed.add_field(name=name, value=value, inline=False)
