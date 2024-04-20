"""Skeleton Configs CLI."""

from dataclasses import dataclass, field
import datetime
import json
import os


import click

from skeleton import database
from skeleton.configs import console, crud, models, schemas


@dataclass()
class ConfigCmd:
    configs_db: object = None
    debug: bool = False
    test: bool = False


@click.group("configs")
@click.pass_context
def configs(ctx):
    """
    Config commands.
    """
    configs_db = ctx.obj.configs_db
    debug = ctx.obj.debug
    test = ctx.obj.test
    pass


@configs.command("add")
@click.option(
    "-f",
    "--file",
    help="Use JSON file for input",
    default=None,
    type=click.File("rb"),
)
@click.option(
    "-n",
    "--name",
    help="Config name",
    default=None,
    type=str,
)
@click.option(
    "-v",
    "--value",
    help="Config value",
    default=None,
    type=str,
)
@click.pass_obj
def add_config(ctx_obj, file):
    """Add an config to the database."""

    configs_db = ctx_obj.configs_db
    debug = ctx_obj.debug
    test = ctx_obj.test

    if not (name or file):
        console.exit_msg("A Name/Value pair or File must be provided")

    if file:
        config_data = json.load(file)
        ts = datetime.datetime.strptime(config_data["ts"], "%m/%d/%Y %I:%M %p")
        config_data["ts"] = ts
    else:
        ts = datetime.datetime.now().replace(second=0, microsecond=0)
        config_data = { "name": name, "value": value, "ts": ts }

    if debug:
        console.console.print_json(data={"config_data": config_data})

    f = schemas.ConfigAdd(
        name=str(config_data["name"]),
        value=str(config_data["value"]),
        ts=ts,                          # timestamp
    )
    crud.add_config(configs_db, debug, f)


@configs.command("list")
@click.option(
    "-m",
    "--minimal",
    is_flag=True,
    default=False,
    help="Use minimal format for copy/pasting.",
)
@click.option(
    "-n",
    "--name",
    help="Search for matching config names.",
    default=None,
    type=str,
)
@click.pass_obj
def list_configs(ctx_obj, minimal, name):
    """List configs in database."""

    configs_db = ctx_obj.configs_db
    debug = ctx_obj.debug
    test = ctx_obj.test

    if name:
        configs = crud.get_configs_by_match(configs_db, name)
    else:
        configs = crud.get_configs(configs_db)

    if name and not configs:
        console.exit_msg("no matching name found")

    if minimal:
        console.display_configs_minimal(configs)
    else:
        console.display_configs(configs)


@configs.command("update")
@click.option(
    "-f",
    "--file",
    help="Use JSON file for input",
    default=None,
    type=click.File("rb"),
)
@click.option(
    "-i",
    "--config-id",
    help="Update the matching config id",
    required=True,
    type=str,
)
@click.option(
    "-n",
    "--config-name",
    help="Update the matching config name",
    default=None,
    type=str,
)
@click.option(
    "-v",
    "--config-value",
    help="Update the matching config name's value",
    default=None,
    type=str,
)
@click.pass_obj
def update_config(ctx_obj, file, config_id, config_name, config_value):
    """Update an config in the database."""

    if not config_id:
        console.exit_msg("Need to provide a config id to update")

    configs_db = ctx_obj.configs_db
    debug = ctx_obj.debug
    test = ctx_obj.test

    if not (config_name or file):
        console.exit_msg("A Name/Value pair or File must be provided")

    if file:
        config_data = json.load(file)
        ts = datetime.datetime.strptime(config_data["ts"], "%m/%d/%Y %I:%M %p")
        config_data["ts"] = ts
    else:
        ts = datetime.datetime.now().replace(second=0, microsecond=0)
        config_data = { "name": config_name, "value": config_value, "ts": ts }

    if not config_id:
        config = crud.get_config_by_match(configs_db, config_data["name"])
        config_id = config.id
    else:
        config = crud.get_config(configs_db, config_id)

    if config:
        if not config_value and config.value:
            config_data["value"] = config.value

    if debug:
        console.debug_msg(config_id)
        console.debug_msg(config_data)

    f = schemas.ConfigUpdate(
        name=str(config_data["name"]),
        value=str(config_data["value"]),
        ts=ts,                          # timestamp
    )
    crud.update_config(configs_db, debug, config_id, f)


@configs.command("delete")
@click.option(
    "-i",
    "--config-id",
    help="Delete the matching config id",
    default=None,
    type=str,
)
@click.option(
    "-n",
    "--config-name",
    help="Delete the matching config name",
    default=None,
    type=str,
)
@click.pass_obj
def delete_config(ctx_obj, config_id, config_name):
    """Delete an config from the database."""

    if not config_id and not config_name:
        console.exit_msg("Need to provide either an config id or a name for matching")

    configs_db = ctx_obj.configs_db
    debug = ctx_obj.debug
    test = ctx_obj.test

    if config_name:
        config_id = crud.get_config_by_match(configs_db, config_name).id

    if debug:
        console.console.print_json(data={"config_id": config_id})

    crud.delete_config(configs_db, debug, config_id)


if __name__ == "__main__":
    configs()
