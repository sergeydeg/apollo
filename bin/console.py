import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append("..")
from event_bot.models import *

engine = create_engine('sqlite:///memory')
Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)
session = Session()
