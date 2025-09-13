"""populate configs

Revision ID: 2
Revises: 1
Create Date: 2025-09-13 13:39:07.488758

"""
import datetime
import json
import os

from typing import Sequence, Union

from alembic import op

from skeleton.models import Config

# revision identifiers, used by Alembic.
revision: str = "2"
down_revision: Union[str, None] = "1"
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
