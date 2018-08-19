import discord


class HelpEmbed:

    def __init__(self, prefix, commands):
        self.prefix = prefix
        self.commands = commands


    def call(self):
        embed = discord.Embed(title="Available Commands")

        for command in self._visible_commands():
            signature = self._get_command_signature(command)
            help_text = self._get_command_help_text(command)
            embed.add_field(name=signature, value=help_text, inline=False)

        return embed


    def _visible_commands(self):
        return filter(lambda cmd: cmd.hidden == False, self.commands)


    def _get_command_help_text(self, command):
        """Use the first block of text for the short help message"""
        return command.help.split('\n')[0]


    def _get_command_signature(self, command):
        return self.prefix + command.name
