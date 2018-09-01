import arrow
import discord

from apollo import emojis as emoji
from apollo.constants import EMBED_COLOR
from apollo.time_zones import VALID_TIME_ZONES


ACCEPTED_HEADER = "Accepted"
ALTERNATE_HEADER = "Alternate"
DECLINED_HEADER = "Declined"


def event_embed(guild, event):
    """Create a Discord Embed to represent an event message"""
    embed = discord.Embed()
    embed.color = EMBED_COLOR
    embed.title = event.title

    if event.description:
        embed.description = event.description

    embed.set_footer(
        text=f"Created by {_organizer_name(guild, event)} | " \
             f"React with {emoji.SKULL} to remove this event"
    )

    # Start time field
    embed.add_field(
        name="Time",
        value=_format_start_time(event),
        inline=False
    )

    # Attendance fields
    embed.add_field(
        name=_accepted_header(event),
        value=_format_attendees(guild, event, "accepted")
    )
    embed.add_field(
        name=DECLINED_HEADER,
        value=_format_attendees(guild, event, "declined")
    )
    embed.add_field(
        name=ALTERNATE_HEADER,
        value=_format_attendees(guild, event, "alternate")
    )

    return embed


def _format_attendees(guild, event, status):
    """Create a formatted list of attendess with given status"""
    members = _members_by_status(guild, event.responses, status)
    return _format_members(members)


def _format_start_time(event):
    start_time = event.local_start_time.format("ddd MMM Do, YYYY @ h:mm A")
    return f"{start_time} {event.time_zone}"


def _accepted_header(event):
    """If there is an event capacity set, create the appropriate header"""
    header = ACCEPTED_HEADER
    if event.capacity:
        responses = list(
            filter(lambda r: r.status == "accepted", event.responses)
        )
        accepted_count = len(responses)
        header += f" ({accepted_count}/{event.capacity})"
    return header


def _attendee_ids_by_status(responses, status):
    """Get the user id of attendees with the given status"""
    responses = filter(lambda r: r.status == status, responses)
    return map(lambda r: r.user_id, responses)


def _members_by_status(guild, responses, status):
    """Retrieve all guild members with the given status"""
    members = []
    for user_id in _attendee_ids_by_status(responses, status):
        member = guild.get_member(user_id)
        if member:
            members.append(member)
    return members


def _format_members(members):
    """Format the given list of members"""
    formatted_list = ""
    for member in members:
        formatted_list += f"{member.display_name}\n"
    if len(formatted_list) == 0:
        formatted_list = "-"
    return formatted_list


def _organizer_name(guild, event):
    """Retrieve the guild specific display name of the organizer"""
    organizer = guild.get_member(event.organizer_id)
    if organizer:
        return organizer.display_name
    else:
        return "Unknown User"
