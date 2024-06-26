"""populate configs

Revision ID: 67ef9cbe1976
Revises: 9d5bca9a7d3e
Create Date: 2023-10-29 14:33:01.488758

"""
import datetime
import json
import os

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from skeleton.configs.models import Config

# revision identifiers, used by Alembic.
revision: str = '67ef9cbe1976'
down_revision: Union[str, None] = '9d5bca9a7d3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    configs = []
    for config_file in sorted(os.listdir("json/configs")):
        with open(os.path.join("json/configs", config_file), "r") as f:
            config_data = json.load(f)
            configs.append(
                dict(
                    id=None,
                    name=config_data["name"],
                    value=config_data["value"],
                    ts=datetime.datetime.now().replace(second=0, microsecond=0),
                )
            )
    op.bulk_insert(Config.__table__, configs)

def downgrade() -> None:
    pass
