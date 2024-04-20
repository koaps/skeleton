"""populate configs

Revision ID: 2
Revises: 1
Create Date: 2022-04-26 17:02:01.031834

"""
from alembic import op
from skeleton.configs.models import Config
import json
import os
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = "2"
down_revision = "1"
branch_labels = None
depends_on = None


def upgrade():
    configs = []
    for config_file in sorted(os.listdir("json/test_configs")):
        with open(os.path.join("json/test_configs", config_file), "r") as f:
            config_data = json.load(f)
            ts = datetime.datetime.strptime(config_data["ts"], "%m/%d/%Y %I:%M %p")
            configs.append(
                dict(
                    id=None,
                    name=config_data["name"],
                    value=config_data["value"],
                    ts=ts,
                )
            )
    op.bulk_insert(Config.__table__, configs)


def downgrade():
    pass
