from discord.errors import Forbidden

from apollo.models import User, Response


class SendEventReminders:
    def __init__(self, bot, reminder_embed):
        self.bot = bot
        self.reminder_embed = reminder_embed

    async def call(self, event):
        with self.bot.scoped_session() as session:
            apollo_users = (
                session.query(User)
                .join(Response)
                .filter(Response.event_id == event.id)
                .filter(Response.status == "accepted")
                .all()
            )

        for apollo_user in apollo_users:
            # If the user has set a time zone, let's make their life a bit easier
            if apollo_user.time_zone:
                start_time = event.localized_start_time(apollo_user.time_zone)
            else:
                start_time = event.local_start_time

            embed = self.reminder_embed.call(event.title, start_time)
            discord_user = self.bot.get_user(apollo_user.id)

            try:
                await discord_user.send(embed=embed)
            except Forbidden:
                pass
