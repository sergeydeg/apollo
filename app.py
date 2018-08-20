import os
from pathlib import Path

import bugsnag
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from apollo import *
from apollo.commands import * 
from apollo.events import *

# Load .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

env = os.getenv('ENV', 'develop')
db_user = os.getenv('DB_USER', 'root')
db_pass = os.getenv('DB_PASS', '')
db_name = os.getenv('DB_NAME', 'apollo')
bugsnag_key = os.getenv('BUGSNAG_KEY')

if env == 'production':
    bugsnag.configure(
        api_key=os.getenv('BUGSNAG_KEY'),
        project_root="./",
    )

engine = create_engine(f'mysql://{db_user}:{db_pass}@localhost/{db_name}?charset=utf8mb4', pool_recycle=3600)
if env == 'develop':
    engine.echo = True

Session = sessionmaker()
Session.configure(bind=engine)

apollo = Apollo(Session)

# Add events
apollo.add_cog(OnGuildChannelDelete(apollo))
apollo.add_cog(OnRawReactionAdd(apollo))
apollo.add_cog(OnReady(apollo))

# Add commands
apollo.add_cog(ChannelCommand(apollo))
apollo.add_cog(EventCommand(apollo))
apollo.add_cog(HelpCommand(apollo))

apollo.run(os.getenv('BOT_TOKEN'))
