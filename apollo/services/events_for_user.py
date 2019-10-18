from apollo.models import Event, EventChannel, Guild, User
from apollo.permissions import HavePermission


class EventsForUser:
    """Get a list of events that a user owns or has write permissions for"""

    def __init__(self, bot):
        """
        :param bot: apollo.apollo.Apollo
        """
        self.bot = bot

    def call(self, discord_member, discord_guild):
        """
        :param discord_member: discord.member.Member
        :param disocrd_guild: apollo.models.guild.Guild
        :return: list[apollo.models.event.Event]
        """
        with self.bot.scoped_session() as session:
            if HavePermission(discord_member, discord_guild).manage_guild():
                return (
                    session.query(Event)
                    .join(EventChannel)
                    .join(Guild)
                    .filter(Guild.id == discord_guild.id)
                    .all()
                )

            return (
                session.query(Event)
                .join(EventChannel)
                .join(Guild)
                .join(User)
                .filter(Guild.id == discord_guild.id)
                .filter(Event.organizer_id == discord_member.id)
                .all()
            )
