import arrow
import discord

from apollo import emojis as emoji
from apollo.constants import EMBED_COLOR
from apollo.time_zones import VALID_TIME_ZONES


class EventEmbed:

    ACCEPTED_HEADER = "Accepted"
    ALTERNATE_HEADER = "Alternate"
    DECLINED_HEADER = "Declined"


    def __init__(self, guild, event):
        self.guild = guild
        self.event = event


    def call(self):
        """Create a Discord Embed to represent an event message"""
        embed = discord.Embed()
        embed.color = EMBED_COLOR
        embed.title = self.event.title

        if self.event.description:
            embed.description = self.event.description

        embed.set_footer(
            text=f"Created by {self._organizer_name()} | " \
                 f"React with {emoji.SKULL} to remove this event"
        )

        # Start time field
        embed.add_field(
            name="Time",
            value=self._formatted_start_time(),
            inline=False
        )

        # Attendance fields
        embed.add_field(
            name=self._accepted_header(),
            value=self._accepted_users()
        )
        embed.add_field(
            name=self.DECLINED_HEADER,
            value=self._declined_users()
        )
        embed.add_field(
            name=self.ALTERNATE_HEADER,
            value=self._alternate_users()
        )

        return embed


    def _accepted_users(self):
        user_ids = self.event.accepted_user_ids
        members = self._user_ids_to_members(user_ids)
        return self._format_members(members)


    def _declined_users(self):
        user_ids = self.event.declined_user_ids
        members = self._user_ids_to_members(user_ids)
        return self._format_members(members)


    def _alternate_users(self):
        user_ids = self.event.alternate_user_ids
        members = self._user_ids_to_members(user_ids)
        return self._format_members(members)


    def _formatted_start_time(self):
        start_time = self.event.local_start_time.format(
            "ddd MMM Do, YYYY @ h:mm A"
            )
        return f"{start_time} {self.event.time_zone}"


    def _accepted_header(self):
        """If there is an event capacity set, create the appropriate header"""
        header = self.ACCEPTED_HEADER
        if self.event.capacity:
            accepted_count = len(self.event.accepted_user_ids)
            header += f" ({accepted_count}/{self.event.capacity})"
        return header


    def _user_ids_to_members(self, user_ids):
        """Convert a list of user_ids to a list of Members"""
        members = []
        for user_id in user_ids:
            member = self.guild.get_member(user_id)
            if member:
                members.append(member)
            else:
                members.append("Unknown User")
        return members


    def _format_members(self, members):
        """Format the given list of members"""
        formatted_list = ""
        for member in members:
            formatted_list += f"{member.display_name}\n"
        if len(formatted_list) == 0:
            formatted_list = "-"
        return formatted_list


    def _organizer_name(self):
        """Retrieve the guild specific display name of the organizer"""
        organizer = self.guild.get_member(self.event.organizer_id)
        if organizer:
            return organizer.display_name
        else:
            return "Unknown User"
