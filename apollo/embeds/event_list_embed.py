import discord

from apollo.constants import EMBED_COLOR
from apollo.translate import t


class EventListEmbed:
    def call(self, events, title):
        embed = discord.Embed(title=title)
        embed.colour = EMBED_COLOR
        embed.description = self._create_events_string(events)
        embed.set_footer(text=t("event.selection_cancel"))
        return embed

    def _create_events_string(self, events):
        """Creates embed description"""
        events_string = ""
        for index, event in enumerate(events, start=1):
            events_string += f"**{index}** {event.title}\n"

        return events_string
