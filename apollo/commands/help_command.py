from discord.ext import commands

from apollo.embeds import HelpEmbed


class HelpCommand(commands.Cog):
    def __init__(self, bot, help_embed):
        self.bot = bot
        self.help_embed = help_embed

        # Remove default help command
        self.bot.remove_command("help")

    @commands.command(hidden=True)
    async def help(self, ctx):
        visible_commands = filter(lambda cmd: cmd.hidden == False, self.bot.commands)
        help_embed = self.help_embed.call(ctx.prefix, visible_commands)
        await ctx.send(embed=help_embed)
