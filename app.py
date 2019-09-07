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
from apollo.input import *

# Load .env file
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

env = os.getenv("ENV", "develop")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_name = os.getenv("DB_NAME")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

engine = create_engine(
    f"mysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?charset=utf8mb4",
    pool_recycle=3600,
)

if env == "develop":
    engine.echo = True

# Configure session factory
Session = sessionmaker(expire_on_commit=False)
Session.configure(bind=engine)
scoped_session = ScopedSession(Session)

# Setup cache
cache = Cache(Session)
cache.load_prefixes()

# Initialize bot
apollo = Apollo(Session, cache)

# Initialze input services
time_zone_input = TimeZoneInput(apollo)

# Initialize embeds
about_embed = AboutEmbed()
event_embed = EventEmbed()
help_embed = HelpEmbed()
start_time_embed = StartTimeEmbed()
time_zone_embed = TimeZoneEmbed()

# Initialize services
format_date_time = FormatDateTime()
request_local_start_time = RequestLocalStartTime(scoped_session, format_date_time, time_zone_input, time_zone_embed, start_time_embed)
update_event = UpdateEvent(apollo, event_embed)
update_response = UpdateResponse(apollo)
sync_event_channels = SyncEventChannels(apollo)
list_event = ListEvent(apollo, event_embed)
list_events = ListEvents(apollo, list_event)
handle_event_reaction = HandleEventReaction(
    apollo, update_event, update_response, request_local_start_time
)

# Add events
apollo.add_cog(OnCommandError(apollo))
apollo.add_cog(OnGuildChannelDelete(apollo))
apollo.add_cog(OnGuildJoin(apollo))
apollo.add_cog(OnGuildRemove(apollo))
apollo.add_cog(OnRawMessageDelete(apollo))
apollo.add_cog(OnRawReactionAdd(apollo, handle_event_reaction))
apollo.add_cog(OnReady(apollo))

# Add commands
apollo.add_cog(AboutCommand(apollo, about_embed))
apollo.add_cog(ChannelCommand(apollo, list_events))
apollo.add_cog(EventCommand(apollo, list_events, sync_event_channels))
apollo.add_cog(HelpCommand(apollo, help_embed))
apollo.add_cog(PrefixCommand(apollo))
apollo.add_cog(RoleCommand(apollo))
apollo.add_cog(TimeZoneCommand(apollo, time_zone_embed, time_zone_input))

# Add checks
apollo.add_check(NotEventChannel(apollo))

# Add tasks
if env == "production":
    apollo.add_cog(SyncDiscordBots(apollo, dbl.Client(apollo, os.getenv("DBL_TOKEN"))))

apollo.run(os.getenv("BOT_TOKEN"), reconnect=True)
