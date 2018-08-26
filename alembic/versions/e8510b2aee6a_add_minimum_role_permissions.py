"""Add minimum role permissions

Revision ID: e8510b2aee6a
Revises: e7b12081a0bc
Create Date: 2018-08-26 09:50:20.267453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8510b2aee6a'
down_revision = 'e7b12081a0bc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('guilds', sa.Column('event_role_id', sa.BigInteger)) 
    op.add_column('guilds', sa.Column('channel_role_id', sa.BigInteger)) 
    op.add_column('guilds', sa.Column('delete_role_id', sa.BigInteger)) 


def downgrade():
    op.drop_column('guilds', 'event_role_id')
    op.drop_column('guilds', 'channel_role_id')
    op.drop_column('guilds', 'delete_role_id')
