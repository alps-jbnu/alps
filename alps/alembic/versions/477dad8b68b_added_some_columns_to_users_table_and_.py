"""Added some columns to users table and update columns

Revision ID: 477dad8b68b
Revises: 21280ec32ea
Create Date: 2015-03-04 22:16:56.433495

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '477dad8b68b'
down_revision = '21280ec32ea'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users',
                  sa.Column('department', sa.String(), nullable=True))
    op.add_column('users',
                  sa.Column('description', sa.String(), nullable=True))
    op.add_column('users',
                  sa.Column('is_jbnu_student', sa.Boolean(), nullable=False,
                            server_default='0'))
    op.add_column('users',
                  sa.Column('student_number', sa.String(), nullable=True))
    op.alter_column('users', 'name',
                    existing_type=sa.String(),
                    nullable=True)
    op.create_index(op.f('ix_users_department'), 'users',
                    ['department'], unique=False)
    op.create_index(op.f('ix_users_is_jbnu_student'), 'users',
                    ['is_jbnu_student'], unique=False)
    op.create_index(op.f('ix_users_student_number'), 'users',
                    ['student_number'], unique=False)
    op.drop_index('ix_users_email', table_name='users')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    op.drop_index(op.f('ix_users_student_number'), table_name='users')
    op.drop_index(op.f('ix_users_is_jbnu_student'), table_name='users')
    op.drop_index(op.f('ix_users_department'), table_name='users')
    op.alter_column('users', 'name',
                    existing_type=sa.String(),
                    nullable=False)
    op.drop_column('users', 'student_number')
    op.drop_column('users', 'is_jbnu_student')
    op.drop_column('users', 'description')
    op.drop_column('users', 'department')
