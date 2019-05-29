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


    def call(self, event, guild):
        """Create a Discord Embed to represent an event message"""
        embed = discord.Embed()
        embed.color = EMBED_COLOR
        embed.title = event.title

        if event.description:
            embed.description = event.description

        embed.set_footer(
            text=t("event.created_by").format(
                self._organizer_name(event, guild),
                emoji.SKULL
            )
        )

        # Start time field
        embed.add_field(
            name=t("event.time"),
            value=self._formatted_start_time(event),
            inline=False
        )

        # Attendance fields
        embed.add_field(
            name=self._accepted_header(event),
            value=self._accepted_users(event, guild)
        )
        embed.add_field(
            name=self.DECLINED_HEADER,
            value=self._declined_users(event, guild)
        )
        embed.add_field(
            name=self.TENTATIVE_HEADER,
            value=self._tentative_users(event, guild)
        )

        # If there is an overflow of users, display them
        standby_users = self._standby_users(event, guild)
        if standby_users != "-":
            embed.add_field(
                name=self.STANDBY_HEADER,
                value=standby_users
            )

        return embed


    def _accepted_users(self, event, guild):
        user_ids = event.accepted_user_ids
        members = self._user_ids_to_members(user_ids, guild)
        return self._format_members(members)


    def _declined_users(self, event, guild):
        user_ids = event.declined_user_ids
        members = self._user_ids_to_members(user_ids, guild)
        return self._format_members(members)


    def _tentative_users(self, event, guild):
        user_ids = event.tentative_user_ids
        members = self._user_ids_to_members(user_ids, guild)
        return self._format_members(members)


    def _standby_users(self, event, guild):
        user_ids = event.standby_user_ids
        members = self._user_ids_to_members(user_ids, guild)
        return self._format_members(members)


    def _formatted_start_time(self, event):
        start_time = event.local_start_time.format(
            "ddd MMM Do, YYYY @ h:mm A"
            )
        time_zone = event.local_start_time.tzname()
        return f"{start_time} {time_zone}"


    def _accepted_header(self, event):
        """If there is an event capacity set, create the appropriate header"""
        header = self.ACCEPTED_HEADER
        if event.capacity:
            accepted_count = len(event.accepted_user_ids)
            header += f" ({accepted_count}/{event.capacity})"
        return header


    def _user_ids_to_members(self, user_ids, guild):
        """Convert a list of user_ids to a list of Members"""
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
