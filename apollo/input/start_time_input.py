import arrow

from apollo.translate import t


class StartTimeInput:
    def __init__(self, bot):
        self.bot = bot

    async def call(self, user, channel, iso_time_zone, update=False):
        """
        Retrieve a datetime UTC object from the user
        :param user: Member, e.g. context.author
        :param channel: Messageable, e.g. context.author.dmchannel
        :param iso_time_zone: str, Option in Apollo.time_zones.ISO_TIME_ZONES
        :return: Arrow object
        """
        while True:
            start_time_str = (
                await self.bot.get_next_message(user, channel)
            ).content.upper()
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
                    await user.send(t("event.start_time_in_the_past"))
                else:
                    return utc_start_time
            except:
                await user.send(t("event.invalid_start_time"))
