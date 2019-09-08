from apollo.translate import t


MAX_CAPACITY = 40


class CapacityInput:
    def __init__(self, bot):
        self.bot = bot

    async def call(self, ctx):
        """Retrieve the event capacity from the user"""
        await ctx.author.send(t("event.capacity_prompt"))
        while True:
            resp = (await self.bot.get_next_pm(ctx.author)).content
            if resp.upper() == "NONE":
                return None
            elif resp.isdigit() and int(resp) in range(1, MAX_CAPACITY):
                return int(resp)
            else:
                await ctx.author.send(t("event.invalid_capacity").format(MAX_CAPACITY))
