import discord

from apollo import emojis as emoji
from apollo.constants import EMBED_COLOR
from apollo.translate import t


class EventEmbed:

    ACCEPTED_HEADER = t("event.accepted")
    TENTATIVE_HEADER = t("event.tentative")
    DECLINED_HEADER = t("event.declined")
    STANDBY_HEADER = t("event.standby")

    def __init__(self):
        pass

    def call(self, event_summary):
        """Create a Discord Embed to represent an event message"""
        embed = discord.Embed()
        embed.color = EMBED_COLOR
        embed.title = event_summary.title

        if event_summary.description:
            embed.description = event_summary.description

        embed.set_footer(
            text=t("event.created_by").format(
                self._organizer_name(event_summary.organizer()), emoji.SKULL
            )
        )

        # Start time field
        embed.add_field(
            name=t("event.time"), value=event_summary.start_time_display(), inline=False
        )

        accepted_members = event_summary.accepted_members()
        embed.add_field(
            name=self._accepted_header(event_summary.capacity, len(accepted_members)),
            value=self._format_members(accepted_members),
        )

        declined_members = event_summary.declined_members()
        embed.add_field(
            name=self.DECLINED_HEADER, value=self._format_members(declined_members)
        )

        tentative_members = event_summary.tentative_members()
        embed.add_field(
            name=self.TENTATIVE_HEADER, value=self._format_members(tentative_members)
        )

        standby_members = event_summary.standby_members()
        if len(standby_members) > 0:
            embed.add_field(
                name=self.STANDBY_HEADER, value=self._format_members(standby_members)
            )

        return embed

    def _accepted_header(self, event_capacity, accepted_count):
        header = self.ACCEPTED_HEADER

        if event_capacity:
            return f"{header} ({accepted_count}/{event_capacity})"

        if accepted_count > 0:
            return f"{header} ({accepted_count})"

        return header

    def _format_members(self, members):
        """Format the given list of members"""
        formatted_list = ""
        for member in members:
            formatted_list += f"{member.display_name}\n"
        if len(formatted_list) == 0:
            formatted_list = "-"
        return formatted_list

    def _organizer_name(self, organizer):
        """Retrieve the guild specific display name of the organizer"""
        if organizer:
            return organizer.display_name
        else:
            return t("event.unknown_user")
