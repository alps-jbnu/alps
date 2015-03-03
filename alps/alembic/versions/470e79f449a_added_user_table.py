"""Added user table

Revision ID: 470e79f449a
Revises:
Create Date: 2015-01-20 09:15:29.833873

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '470e79f449a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('users')
