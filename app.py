import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from apollo import *
from apollo.checks import *
from apollo.commands import * 
from apollo.events import *

# Load .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

env = os.getenv('ENV', 'develop')
db_user = os.getenv('DB_USER', 'root')
db_pass = os.getenv('DB_PASS', '')
db_name = os.getenv('DB_NAME', 'apollo')

engine = create_engine(f'mysql://{db_user}:{db_pass}@localhost/{db_name}?charset=utf8mb4', pool_recycle=3600)
if env == 'develop':
    engine.echo = True

# Configure session factory
Session = sessionmaker()
Session.configure(bind=engine)

# Setup cache
cache = Cache(Session)

# Initialize bot
apollo = Apollo(Session, cache)

# Add events
apollo.add_cog(OnCommandError(apollo))
apollo.add_cog(OnGuildChannelDelete(apollo))
apollo.add_cog(OnGuildJoin(apollo))
apollo.add_cog(OnGuildRemove(apollo))
apollo.add_cog(OnMessage(apollo))
apollo.add_cog(OnRawMessageDelete(apollo))
apollo.add_cog(OnRawReactionAdd(apollo))
apollo.add_cog(OnReady(apollo))

# Add commands
apollo.add_cog(AboutCommand(apollo))
apollo.add_cog(ChannelCommand(apollo))
apollo.add_cog(EventCommand(apollo))
apollo.add_cog(HelpCommand(apollo))
apollo.add_cog(PrefixCommand(apollo))
apollo.add_cog(RoleCommand(apollo))

# Add checks
apollo.add_check(NotEventChannel(apollo))

# Migrate, temporary
from apollo.models import Event
from apollo.time_zones import VALID_TIME_ZONES
session = Session()
for event in session.query(Event).all():
    event.time_zone = VALID_TIME_ZONES[event.time_zone]
session.commit()

apollo.run(os.getenv('BOT_TOKEN'))
