# This file contains the global scope of the app

import os
import discord
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import *
from .events import *
from .commands import *

db_user = os.getenv('DB_USER', 'root')
db_pass = os.getenv('DB_PASS', '')

engine = create_engine(f'mysql://{db_user}:{db_pass}@localhost/event_bot')
Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)

bot = discord.ext.commands.Bot(command_prefix='!')

bot.add_cog(OnReady(bot))
bot.add_cog(Ping(bot))
