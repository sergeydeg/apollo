from discord.errors import Forbidden

class RequestLocalStartTime:
    def __init__(self, scoped_session, format_date_time, prompt_time_zone):
        self.scoped_session = scoped_session
        self.format_date_time = format_date_time
        self.prompt_time_zone = prompt_time_zone

    async def call(self, apollo_user, discord_user, utc_start_time):
        if not apollo_user.time_zone:
            apollo_user.time_zone = await self.prompt_time_zone.call(discord_user)
            with self.scoped_session.call() as session:
                session.add(apollo_user)

        local_start_time = utc_start_time.to(apollo_user.time_zone)
        formatted_local_start_time = self.format_date_time.call(local_start_time)

        try:
            await discord_user.send(formatted_local_start_time)
        except Forbidden:
            pass
