"""Initial revision

Revision ID: 56c02a15aac
Revises:
Create Date: 2015-03-15 21:47:36.852762

"""

from alembic import op
import sqlalchemy as sa

revision = '56c02a15aac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create 'users' table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('nickname', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('pwhash', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=100), nullable=True),
        sa.Column('is_jbnu_student', sa.Boolean(), nullable=False),
        sa.Column('student_number', sa.String(length=100), nullable=True),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('email_validated', sa.Boolean(), nullable=False),
        sa.Column('confirm_token', sa.String(length=100), nullable=True),
        sa.Column('member_type', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_confirm_token'),
                    'users', ['confirm_token'], unique=False)
    op.create_index(op.f('ix_users_created_at'),
                    'users', ['created_at'], unique=False)
    op.create_index(op.f('ix_users_email'),
                    'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_name'),
                    'users', ['name'], unique=False)
    op.create_index(op.f('ix_users_nickname'),
                    'users', ['nickname'], unique=True)
    op.create_index(op.f('ix_users_username'),
                    'users', ['username'], unique=True)

    # Create 'boards' table
    op.create_table(
        'boards',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('text', sa.String(length=100), nullable=False),
        sa.Column('read_permission', sa.Integer(), nullable=False),
        sa.Column('write_permission', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_boards_name'), 'boards', ['name'], unique=True)

    # Create 'posts' table
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('board_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['board_id'], ['boards.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_board_id'),
                    'posts', ['board_id'], unique=False)
    op.create_index(op.f('ix_posts_created_at'),
                    'posts', ['created_at'], unique=False)
    op.create_index(op.f('ix_posts_title'),
                    'posts', ['title'], unique=False)
    op.create_index(op.f('ix_posts_user_id'),
                    'posts', ['user_id'], unique=False)


def downgrade():
    # Drop 'posts' table
    op.drop_index(op.f('ix_posts_user_id'), table_name='posts')
    op.drop_index(op.f('ix_posts_title'), table_name='posts')
    op.drop_index(op.f('ix_posts_created_at'), table_name='posts')
    op.drop_index(op.f('ix_posts_board_id'), table_name='posts')
    op.drop_table('posts')

    # Drop 'boards' table
    op.drop_index(op.f('ix_boards_name'), table_name='boards')
    op.drop_table('boards')

    # Drop 'users' table
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_nickname'), table_name='users')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_created_at'), table_name='users')
    op.drop_index(op.f('ix_users_confirm_token'), table_name='users')
    op.drop_table('users')
