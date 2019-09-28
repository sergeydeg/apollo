import arrow
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

    def call(self, event, responses, guild):
        """Create a Discord Embed to represent an event message"""
        embed = discord.Embed()
        embed.color = EMBED_COLOR
        embed.title = event.title

        if event.description:
            embed.description = event.description

        embed.set_footer(
            text=t("event.created_by").format(
                self._organizer_name(event, guild), emoji.SKULL
            )
        )

        # Start time field
        embed.add_field(
            name=t("event.time"), value=event.start_time_string(), inline=False
        )

        accepted_members = self._accepted_members(responses, guild, event.capacity)
        embed.add_field(
            name=self._accepted_header(event.capacity, len(accepted_members)),
            value=self._format_members(accepted_members),
        )

        declined_members = self._declined_members(responses, guild)
        embed.add_field(
            name=self.DECLINED_HEADER, value=self._format_members(declined_members)
        )

        tentative_members = self._tentative_members(responses, guild)
        embed.add_field(
            name=self.TENTATIVE_HEADER, value=self._format_members(tentative_members)
        )

        standby_members = self._standby_members(responses, guild, event.capacity)
        if len(standby_members) > 0:
            embed.add_field(
                name=self.STANDBY_HEADER, value=self._format_members(standby_members)
            )

        return embed

    def _accepted_members(self, responses, guild, event_capacity):
        user_ids = self._user_ids_by_status(responses, "accepted")[:event_capacity]
        return self._user_ids_to_members(user_ids, guild)

    def _declined_members(self, responses, guild):
        user_ids = self._user_ids_by_status(responses, "declined")
        return self._user_ids_to_members(user_ids, guild)

    def _tentative_members(self, responses, guild):
        user_ids = self._user_ids_by_status(responses, "alternate")
        return self._user_ids_to_members(user_ids, guild)

    def _standby_members(self, responses, guild, event_capacity):
        if not event_capacity:
            return []
        user_ids = self._user_ids_by_status(responses, "accepted")[event_capacity:]
        return self._user_ids_to_members(user_ids, guild)

    def _accepted_header(self, event_capacity, accepted_count):
        header = self.ACCEPTED_HEADER

        if event_capacity:
            return f"{header} ({accepted_count}/{event_capacity})"

        if accepted_count > 0:
            return f"{header} ({accepted_count})"

        return header

    def _user_ids_to_members(self, user_ids, guild):
        members = []
        for user_id in user_ids:
            member = guild.get_member(user_id)
            if member:
                members.append(member)
        return members

    def _format_members(self, members):
        """Format the given list of members"""
        formatted_list = ""
        for member in members:
            formatted_list += f"{member.display_name}\n"
        if len(formatted_list) == 0:
            formatted_list = "-"
        return formatted_list

    def _organizer_name(self, event, guild):
        """Retrieve the guild specific display name of the organizer"""
        organizer = guild.get_member(event.organizer_id)
        if organizer:
            return organizer.display_name
        else:
            return t("event.unknown_user")

    def _user_ids_by_status(self, responses, status):
        filtered_responses = list(filter(lambda r: r.status == status, responses))
        filtered_responses.sort(key=lambda r: r.last_updated)
        return list(map(lambda r: r.user_id, filtered_responses))
