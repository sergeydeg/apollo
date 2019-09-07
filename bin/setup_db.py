import os
import sys

from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from apollo.models import Base

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_name = os.getenv("DB_NAME")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

# Create tables
engine = create_engine(f"mysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
Base.metadata.create_all(engine)

# Stamp latest revision so we don't run migrations on a fresh db
alembic_cfg = Config("alembic.ini")
command.stamp(alembic_cfg, "head")
