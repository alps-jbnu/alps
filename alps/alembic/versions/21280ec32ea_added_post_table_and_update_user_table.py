"""Added post table and update user table

Revision ID: 21280ec32ea
Revises: 470e79f449a
Create Date: 2015-01-25 11:24:32.092617

"""

# revision identifiers, used by Alembic.
revision = '21280ec32ea'
down_revision = '470e79f449a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


# WARNING: not nullable columns added without server_default!!!
def upgrade():
    # create post table
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_posts_title'), 'posts', ['title'], unique=False)

    # update user table
    op.add_column('users', sa.Column('email', sa.String(), nullable=False))
    op.add_column('users', sa.Column('nickname', sa.String(), nullable=False))
    op.add_column('users', sa.Column('pwhash', sa.String(), nullable=False))
    op.add_column('users', sa.Column('username', sa.String(), nullable=False))

    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    op.create_index(op.f('ix_users_nickname'), 'users', ['nickname'],
                    unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'],
                    unique=True)


def downgrade():
    # drop columnss in user table
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_nickname'), table_name='users')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')

    op.drop_column('users', 'username')
    op.drop_column('users', 'pwhash')
    op.drop_column('users', 'nickname')
    op.drop_column('users', 'email')

    # drop post table
    op.drop_index(op.f('ix_posts_title'), table_name='posts')

    op.drop_table('posts')
