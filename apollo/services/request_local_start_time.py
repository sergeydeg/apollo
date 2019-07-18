from discord.errors import Forbidden


class RequestLocalStartTime:
    def __init__(
        self,
        scoped_session,
        format_date_time,
        time_zone_input,
        time_zone_embed,
        start_time_embed,
    ):
        self.scoped_session = scoped_session
        self.format_date_time = format_date_time
        self.time_zone_input = time_zone_input
        self.time_zone_embed = time_zone_embed
        self.start_time_embed = start_time_embed

    async def call(self, apollo_user, discord_user, event):
        if not apollo_user.time_zone:
            try:
                await discord_user.send(embed=self.time_zone_embed.call())
            except Forbidden:
                pass

            apollo_user.time_zone = await self.time_zone_input.call(
                discord_user, discord_user.dm_channel
            )
            with self.scoped_session.call() as session:
                session.add(apollo_user)

        local_start_time = event.utc_start_time.to(apollo_user.time_zone)
        formatted_local_start_time = self.format_date_time.call(local_start_time)

        embed = self.start_time_embed.call(event.title, formatted_local_start_time)
        await discord_user.send(embed=embed)
