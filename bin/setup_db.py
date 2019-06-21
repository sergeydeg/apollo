import os
import sys

from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from apollo.models import Base

db_user = os.getenv("DB_USER", "root")
db_pass = os.getenv("DB_PASS", "")

# Create database
if db_pass:
    os.system(
        f"mysql -u{db_user} -p{db_pass} -e 'create database apollo character set UTF8mb4 collate utf8mb4_bin';"
    )
else:
    os.system(
        f"mysql -u{db_user} -e 'create database apollo character set UTF8mb4 collate utf8mb4_bin';"
    )

# Create tables
engine = create_engine(f"mysql://{db_user}:{db_pass}@localhost/apollo")
Base.metadata.create_all(engine)

# Stamp latest revision so we don't run migrations on a fresh db
alembic_cfg = Config("alembic.ini")
command.stamp(alembic_cfg, "head")
