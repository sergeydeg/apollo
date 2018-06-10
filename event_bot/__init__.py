import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_user = os.getenv('DB_USER', 'root')
db_pass = os.getenv('DB_PASS', '')

engine = create_engine(f'mysql://{db_user}:{db_pass}@localhost/event_bot')
Session = sessionmaker()
Session.configure(bind=engine)
