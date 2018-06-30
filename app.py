import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from event_bot import *
from event_bot.commands import * 
from event_bot.events import *

# Load .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

env = os.getenv('ENV', 'develop')
db_user = os.getenv('DB_USER', 'root')
db_pass = os.getenv('DB_PASS', '')
db_name = os.getenv('DB_NAME', 'event_bot')

engine = create_engine(f'mysql://{db_user}:{db_pass}@localhost/{db_name}?charset=utf8mb4')
if env == 'develop':
    engine.echo = True

Session = sessionmaker(expire_on_commit=False)
Session.configure(bind=engine)
session = Session()

transaction = Transaction(session)
event_bot = EventBot(transaction)

# Add events
event_bot.add_cog(OnRawReactionAdd(event_bot))
event_bot.add_cog(OnReady(event_bot))

# Add commands
event_bot.add_cog(EventCommand(event_bot))

event_bot.run(os.getenv('BOT_TOKEN'))
