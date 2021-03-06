from apollo.embeds import SelectionEmbed
from apollo.translate import t


class SelectionInput:
    def __init__(self, bot):
        self.bot = bot
        self.selection_embed = SelectionEmbed()

    async def call(self, user, channel, selection, title=None, footer=None):
        """
        Send a list of events to the user and ask them to pick one.
        Note only sends a list, and does not send the prompt before it.
        :param user: Member, e.g. context.author
        :param channel: Messageable
        :param selection: dict
        :param title: str or None
        :param footer: str or None
        :return: Event
        """
        if title is None:
            title = t("selection.generic")

        if footer is None:
            footer = t("selection.generic_cancel")

        await channel.send(embed=self.selection_embed.call(selection, title, footer))

        return await self._get_choice_from_user(user, channel, len(selection))

    async def _get_choice_from_user(self, user, channel, valid_range):
        while True:
            resp = (await self.bot.get_next_message(user, channel, timeout=60)).content
            if resp.lower() == "cancel":
                return 0
            if not resp.isdigit() or not 0 < int(resp) <= valid_range:
                await user.send(t("event.invalid_selection_error"))
            else:
                return int(resp)
