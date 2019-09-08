from apollo.translate import t


MAX_DESC_LENGTH = 1000


class DescriptionInput:
    def __init__(self, bot):
        self.bot = bot

    async def call(self, ctx, update=False):
        if update:
            await ctx.author.send(t("event.update_description_prompt"))
        else:
            await ctx.author.send(t("event.description_prompt"))

        while True:
            resp = (await self.bot.get_next_pm(ctx.author, timeout=240)).content
            if len(resp) <= MAX_DESC_LENGTH:
                return resp
            else:
                await ctx.author.send(
                    t("event.invalid_description").format(MAX_DESC_LENGTH)
                )
