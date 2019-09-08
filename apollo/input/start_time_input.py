import arrow

from apollo.translate import t


class StartTimeInput:
    def __init__(self, bot):
        self.bot = bot

    async def call(self, ctx, iso_time_zone, update=False):
        """Retrieve a datetime UTC object from the user"""
        await ctx.author.send(t("event.start_time_prompt"))
        while True:
            start_time_str = (await self.bot.get_next_pm(ctx.author)).content
            if update and start_time_str.upper() == "NONE":
                return None
            try:
                utc_start_time = (
                    arrow.get(
                        start_time_str,
                        ["YYYY-MM-DD h:mm A", "YYYY-MM-DD HH:mm"],
                        tzinfo=iso_time_zone,
                    )
                    .to("utc")
                    .datetime
                )

                if utc_start_time < arrow.utcnow():
                    await ctx.author.send(t("event.start_time_in_the_past"))
                else:
                    return utc_start_time
            except:
                await ctx.author.send(t("event.invalid_start_time"))
