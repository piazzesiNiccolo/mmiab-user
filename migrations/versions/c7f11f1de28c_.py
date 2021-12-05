"""empty message

Revision ID: c7f11f1de28c
Revises: 
Create Date: 2021-12-05 16:40:54.732909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7f11f1de28c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Report',
    sa.Column('id_report', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_reported', sa.Integer(), nullable=True),
    sa.Column('id_signaller', sa.Integer(), nullable=True),
    sa.Column('date_of_report', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id_report')
    )
    op.create_table('User',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.Unicode(length=128), nullable=False),
    sa.Column('first_name', sa.Unicode(length=128), nullable=False),
    sa.Column('last_name', sa.Unicode(length=128), nullable=False),
    sa.Column('nickname', sa.Unicode(length=128), nullable=True),
    sa.Column('location', sa.Unicode(length=128), nullable=True),
    sa.Column('pfp_path', sa.Unicode(length=128), nullable=True),
    sa.Column('content_filter', sa.Boolean(), nullable=True),
    sa.Column('blacklist', sa.Unicode(length=128), nullable=True),
    sa.Column('lottery_points', sa.Integer(), nullable=True),
    sa.Column('is_banned', sa.Boolean(), nullable=True),
    sa.Column('password', sa.Unicode(length=128), nullable=True),
    sa.Column('birthdate', sa.Date(), nullable=True),
    sa.Column('phone', sa.Unicode(length=128), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('authenticated', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('User')
    op.drop_table('Report')
    # ### end Alembic commands ###
