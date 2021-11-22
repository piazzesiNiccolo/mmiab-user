"""empty message

Revision ID: 491db1334358
Revises: 124a8d5f7051
Create Date: 2021-11-20 17:50:44.102002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '491db1334358'
down_revision = '124a8d5f7051'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('User', sa.Column('nickname', sa.Unicode(128), nullable=True))
    op.add_column('User', sa.Column('location', sa.Unicode(128)))
    op.add_column('User', sa.Column('pfp_path', sa.Unicode(128), default="default.png"))
    op.add_column('User', sa.Column('content_filter', sa.Boolean, default=False))
    op.add_column('User', sa.Column('blacklist', sa.Unicode(128)))
    op.add_column('User', sa.Column('lottery_points', sa.Integer, default=0))
    op.add_column('User', sa.Column('is_banned', sa.Boolean, default=False))

def downgrade():
    op.drop_column('User', 'nickname')
    op.drop_column('User', 'location')
    op.drop_column('User', 'pfp_path')
    op.drop_column('User', 'content_filter')
    op.drop_column('User', 'blacklist')
    op.drop_column('User', 'lottery_points')
    op.drop_column('User', 'is_banned')
