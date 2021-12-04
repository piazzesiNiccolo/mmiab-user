"""empty message

Revision ID: 2ad3a98caac6
Revises: 491db1334358
Create Date: 2021-11-24 20:09:14.765451

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "2ad3a98caac6"
down_revision = "491db1334358"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "Report",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.Unicode(length=128), nullable=False),
        sa.Column("first_name", sa.Unicode(length=128), nullable=False),
        sa.Column("last_name", sa.Unicode(length=128), nullable=False),
        sa.Column("password", sa.Unicode(length=128), nullable=True),
        sa.Column("birthdate", sa.Date(), nullable=True),
        sa.Column("phone", sa.Unicode(length=128), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_admin", sa.Boolean(), nullable=True),
        sa.Column("authenticated", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("phone"),
    )


def downgrade():
    pass
