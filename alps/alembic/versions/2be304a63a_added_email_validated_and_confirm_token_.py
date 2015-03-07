"""Added email_validated and confirm_token to users table

Revision ID: 2be304a63a
Revises: 477dad8b68b
Create Date: 2015-03-05 02:53:10.169555

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2be304a63a'
down_revision = '477dad8b68b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('confirm_token',
                                     sa.String(),
                                     nullable=True))
    op.add_column('users', sa.Column('email_validated', sa.Boolean(),
                                     server_default='1', nullable=False))
    op.create_index(op.f('ix_users_confirm_token'), 'users',
                    ['confirm_token'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_users_confirm_token'), table_name='users')
    op.drop_column('users', 'email_validated')
    op.drop_column('users', 'confirm_token')
