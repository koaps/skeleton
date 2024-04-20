"""create config db

Revision ID: 9d5bca9a7d3e
Revises: 
Create Date: 2023-10-29 14:29:40.398904

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d5bca9a7d3e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "configs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=True),
        sa.Column("value", sa.String(length=500), nullable=True),
        sa.Column("ts", sa.TIMESTAMP),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

def downgrade() -> None:
    op.drop_table("configs")
