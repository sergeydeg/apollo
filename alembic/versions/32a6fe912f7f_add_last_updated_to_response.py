"""add last updated to response

Revision ID: 32a6fe912f7f
Revises: e8510b2aee6a
Create Date: 2018-09-03 13:31:37.405041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "32a6fe912f7f"
down_revision = "e8510b2aee6a"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("responses", sa.Column("last_updated", sa.DateTime))


def downgrade():
    op.drop_column("responses", "last_updated")
