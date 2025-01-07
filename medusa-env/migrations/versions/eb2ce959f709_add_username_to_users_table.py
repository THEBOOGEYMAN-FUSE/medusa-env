"""Add username to users table

Revision ID: eb2ce959f709
Revises: c871393da748
Create Date: 2025-01-07 04:20:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'eb2ce959f709'
down_revision = 'c871393da748'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the 'username' column to the 'users' table with a default value
    op.add_column('users', sa.Column('username', sa.String(length=100), nullable=False, server_default='default_username'))
    # Remove the default constraint after adding the column
    op.alter_column('users', 'username', server_default=None)


def downgrade() -> None:
    # Remove the 'username' column from the 'users' table
    op.drop_column('users', 'username')

