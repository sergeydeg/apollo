import discord

from apollo.constants import EMBED_COLOR
from apollo.translate import t


class ReminderEmbed:
    def call(self, event_title, start_time):
        embed = discord.Embed()
        embed.color = EMBED_COLOR
        embed.title = t("reminder.title")
        embed.description = self._event_summary(event_title, start_time)
        return embed

    def _event_summary(self, event_title, start_time):
        start_time = self._formatted_start_time(start_time)
        return f"{event_title} - {start_time}"

    def _formatted_start_time(self, start_time):
        time_display = start_time.format("h:mm A")
        time_zone = start_time.tzname()
        return f"{time_display} {time_zone}"
