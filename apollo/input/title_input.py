from apollo.translate import t


MAX_TITLE_LENGTH = 200


class TitleInput:
    def __init__(self, bot):
        self.bot = bot

    async def call(self, ctx, update=False):
        if update:
            await ctx.author.send(t("event.update_title_prompt"))
        else:
            await ctx.author.send(t("event.title_prompt"))

        while True:
            title = (await self.bot.get_next_pm(ctx.author)).content
            if len(title) <= MAX_TITLE_LENGTH:
                return title
            else:
                await ctx.author.send(t("event.invalid_title").format(MAX_TITLE_LENGTH))
