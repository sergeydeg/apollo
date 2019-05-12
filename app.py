import os
from pathlib import Path

import dbl
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from apollo import *
from apollo.checks import *
from apollo.commands import *
from apollo.embeds import *
from apollo.events import *
from apollo.tasks import *
from apollo.services import *

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

# Initialize embeds
event_embed = EventEmbed()

# Initialize services
update_event = UpdateEvent(apollo, event_embed)
update_response = UpdateResponse()
sync_event_channels = SyncEventChannels(apollo)
list_event = ListEvent(apollo, event_embed)
list_events = ListEvents(apollo, list_event)
delete_event = DeleteEvent(apollo, list_events)
handle_event_reaction = HandleEventReaction(
    apollo,
    delete_event,
    update_event,
    update_response
)

# Add events
apollo.add_cog(OnCommandError(apollo))
apollo.add_cog(OnGuildChannelDelete(apollo))
apollo.add_cog(OnGuildJoin(apollo))
apollo.add_cog(OnGuildRemove(apollo))
apollo.add_cog(OnMessage(apollo))
apollo.add_cog(OnRawMessageDelete(apollo, list_events))
apollo.add_cog(OnRawReactionAdd(apollo, handle_event_reaction))
apollo.add_cog(OnReady(apollo))

# Add commands
apollo.add_cog(AboutCommand(apollo))
apollo.add_cog(ChannelCommand(apollo, list_events))
apollo.add_cog(EventCommand(apollo, list_events, sync_event_channels))
apollo.add_cog(HelpCommand(apollo))
apollo.add_cog(PrefixCommand(apollo))
apollo.add_cog(RoleCommand(apollo))

# Add checks
apollo.add_check(NotEventChannel(apollo))

# Add tasks
if env == 'production':
    apollo.add_cog(
        SyncDiscordBots(apollo, dbl.Client(apollo, os.getenv('DBL_TOKEN')))
    )

apollo.run(os.getenv('BOT_TOKEN'), reconnect=True)
