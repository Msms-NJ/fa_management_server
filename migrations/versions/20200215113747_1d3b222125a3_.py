"""empty message

Revision ID: 1d3b222125a3
Revises: 
Create Date: 2020-02-15 11:37:47.847788

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1d3b222125a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('offices',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('remarks', sa.String(length=128), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('create_by', sa.String(length=64), nullable=True),
    sa.Column('update_by', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('address', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('address'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('remarks', sa.String(length=128), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('create_by', sa.String(length=64), nullable=True),
    sa.Column('update_by', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('remarks', sa.String(length=128), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('create_by', sa.String(length=64), nullable=True),
    sa.Column('update_by', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=True),
    sa.Column('mobile', sa.String(length=32), nullable=True),
    sa.Column('password', sa.Binary(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('address', sa.String(length=256), nullable=True),
    sa.Column('openid', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('mobile'),
    sa.UniqueConstraint('username')
    )
    op.create_table('user_role',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('remarks', sa.String(length=128), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('create_by', sa.String(length=64), nullable=True),
    sa.Column('update_by', sa.String(length=64), nullable=True),
    sa.Column('user_id', postgresql.UUID(), nullable=False),
    sa.Column('role_id', postgresql.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('offices')
    # ### end Alembic commands ###
