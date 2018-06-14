import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from event_bot import EventBot
from event_bot.commands import * 
from event_bot.events import *

db_user = os.getenv('DB_USER', 'root')
db_pass = os.getenv('DB_PASS', '')
db_name = os.getenv('DB_NAME', 'event_bot')

engine = create_engine(f'mysql://{db_user}:{db_pass}@localhost/{db_name}')
Session = sessionmaker()
Session.configure(bind=engine)

bot = EventBot(Session)

# Add events
bot.add_cog(OnReady(bot))

# Add commands
bot.add_cog(Ping(bot))

bot.run(os.getenv('BOT_TOKEN'))
