"""Initial script

Revision ID: 6284417af2
Revises:
Create Date: 2015-03-15 15:21:36.019949

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6284417af2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'boards',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('text', sa.String(length=100), nullable=False),
        sa.Column('read_permission', sa.Integer(), server_default='0',
                  nullable=False),
        sa.Column('write_permission', sa.Integer(), server_default='0',
                  nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('nickname', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('pwhash', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('description', sa.String(length=100), nullable=True),
        sa.Column('is_jbnu_student', sa.Boolean(), server_default='0',
                  nullable=False),
        sa.Column('student_number', sa.String(length=100), nullable=True),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('email_validated', sa.Boolean(), server_default='1',
                  nullable=False),
        sa.Column('confirm_token', sa.String(length=100), nullable=True),
        sa.Column('member_type', sa.Integer(), server_default='0',
                  nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_users_confirm_token'),
                    'users', ['confirm_token'], unique=False)
    op.create_index(op.f('ix_users_department'),
                    'users', ['department'], unique=False)
    op.create_index(op.f('ix_users_email'),
                    'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_is_jbnu_student'),
                    'users', ['is_jbnu_student'], unique=False)
    op.create_index(op.f('ix_users_name'),
                    'users', ['name'], unique=False)
    op.create_index(op.f('ix_users_nickname'),
                    'users', ['nickname'], unique=True)
    op.create_index(op.f('ix_users_student_number'),
                    'users', ['student_number'], unique=False)
    op.create_index(op.f('ix_users_username'),
                    'users', ['username'], unique=True)

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

    op.create_index(op.f('ix_posts_title'), 'posts', ['title'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_posts_title'), table_name='posts')
    op.drop_table('posts')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_student_number'), table_name='users')
    op.drop_index(op.f('ix_users_nickname'), table_name='users')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_is_jbnu_student'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_department'), table_name='users')
    op.drop_index(op.f('ix_users_confirm_token'), table_name='users')
    op.drop_table('users')
    op.drop_table('boards')
