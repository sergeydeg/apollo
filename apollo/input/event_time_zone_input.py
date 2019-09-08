from apollo.embeds.time_zone_embed import TimeZoneEmbed
from apollo.translate import t
from apollo.time_zones import ISO_TIME_ZONES


class EventTimeZoneInput:
    def __init__(self, bot):
        self.bot = bot

    async def call(self, ctx, update=False):
        """Retrieve a valid time zone string from the user"""
        await ctx.author.send(embed=TimeZoneEmbed().call())
        while True:
            resp = (await self.bot.get_next_pm(ctx.author)).content
            if self._valid_time_zone_input(resp):
                time_zone_index = int(resp) - 1
                if time_zone_index in range(len(ISO_TIME_ZONES)):
                    return ISO_TIME_ZONES[time_zone_index]
            else:
                await ctx.author.send(t("event.invalid_time_zone"))

    def _valid_time_zone_input(self, value):
        return value.isdigit() and int(value) in range(1, len(ISO_TIME_ZONES) + 1)
