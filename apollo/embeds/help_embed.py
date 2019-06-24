import discord

from apollo.constants import EMBED_COLOR
from apollo.translate import t


class HelpEmbed:
    INVITE = "https://discord.gg/WKZdqf2"

    def __init__(self):
        pass

    def call(self, prefix, commands):
        embed = discord.Embed(title=t("help.available_commands"))
        embed.color = EMBED_COLOR
        embed.description = t("help.server_invite").format(self.INVITE)

        for command in self._visible_commands(commands):
            signature = prefix + command.name
            help_text = self._get_command_help_text(command)
            embed.add_field(name=signature, value=help_text, inline=False)

        return embed

    def _visible_commands(self, commands):
        return filter(lambda cmd: cmd.hidden == False, commands)

    def _get_command_help_text(self, command):
        """Use the first block of text for the short help message"""
        return command.help.split("\n")[0]
