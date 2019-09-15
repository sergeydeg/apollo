from apollo.time_zones import ISO_TIME_ZONES
from apollo.translate import t


class TimeZoneInput:
    def __init__(self, bot):
        self.bot = bot

    async def call(self, user, channel):
        """
        Retrieve a timezone from the user
        :param user: Member, e.g. context.author
        :param channel: Messageable, e.g. context.author.dmchannel
        :return: str
        """
        all_time_zones = []

        for time_zones in ISO_TIME_ZONES.values():
            for time_zone in time_zones:
                all_time_zones.append(time_zone)

        while True:
            resp = (await self.bot.get_next_message(user, channel)).content

            if not self._valid_time_zone_input(resp, len(all_time_zones)):
                await channel.send(t("event.invalid_time_zone"))
                continue

            time_zone_index = int(resp) - 1
            return all_time_zones[time_zone_index]

    def _valid_time_zone_input(self, value, option_count):
        return value.isdigit() and int(value) in range(1, option_count + 1)
