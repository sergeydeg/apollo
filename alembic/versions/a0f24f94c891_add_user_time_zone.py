"""Add user time zone

Revision ID: a0f24f94c891
Revises: 32a6fe912f7f
Create Date: 2019-06-24 19:19:43.961740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0f24f94c891'
down_revision = '32a6fe912f7f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('time_zone', sa.String(50)))


def downgrade():
    op.drop_column('users', 'time_zone')
