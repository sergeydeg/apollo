import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from event_bot import *
from event_bot.commands import * 
from event_bot.events import *

db_user = os.getenv('DB_USER', 'root')
db_pass = os.getenv('DB_PASS', '')
db_name = os.getenv('DB_NAME', 'event_bot')

engine = create_engine(f'mysql://{db_user}:{db_pass}@localhost/{db_name}?charset=utf8mb4')
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

bot = Bot()
transaction = Transaction(session)
event_bot = EventBot(bot, transaction)

# Add events
bot.add_cog(OnReady(bot, transaction))

# Add commands

event_bot.start(os.getenv('BOT_TOKEN'))
