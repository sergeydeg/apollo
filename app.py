import os
import discord

from event_bot.commands import * 
from event_bot.events import *

bot = discord.ext.commands.Bot(command_prefix='!')

bot.add_cog(OnReady(bot))
bot.add_cog(Ping(bot))

bot.run(os.getenv('BOT_TOKEN'))
