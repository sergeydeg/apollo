import os
from event_bot import bot

bot.run(os.getenv('BOT_TOKEN'))
