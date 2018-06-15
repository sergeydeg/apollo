import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from event_bot import *
from event_bot.commands import * 
from event_bot.events import *

db_user = os.getenv('DB_USER', 'root')
db_pass = os.getenv('DB_PASS', '')
db_name = os.getenv('DB_NAME', 'event_bot')

engine = create_engine(f'mysql://{db_user}:{db_pass}@localhost/{db_name}')
Session = sessionmaker()
Session.configure(bind=engine)

bot = Bot()
session_scope = SessionScope(Session)
event_bot = EventBot(bot, session_scope)

# Add events
bot.add_cog(OnReady(bot, session_scope))

# Add commands

event_bot.start(os.getenv('BOT_TOKEN'))
