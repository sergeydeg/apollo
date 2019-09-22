from apollo.translate import t
from config import MAX_TITLE_LENGTH


class TitleInput:
    def __init__(self, bot):
        self.bot = bot

    async def call(self, user, channel):
        """
        Get title from user
        :param user: Member, e.g. context.author
        :param channel: Messageable, e.g. context.author.dmchannel
        :return: str
        """

        while True:
            title = (await self.bot.get_next_message(user, channel)).content
            if len(title) <= MAX_TITLE_LENGTH:
                return title
            else:
                await user.send(t("event.invalid_title").format(MAX_TITLE_LENGTH))
