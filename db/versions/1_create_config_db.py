"""create config db

Revision ID: 1
Revises: 
Create Date: 2023-10-29 14:29:40.398904

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "configs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("value", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("ts", sa.TIMESTAMP),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

def downgrade() -> None:
    op.drop_table("configs")
