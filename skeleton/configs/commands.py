"""Skeleton Configs CLI."""

from dataclasses import dataclass
import json

import click

from skeleton.configs import console, crud


@dataclass()
class ConfigCmd:
    db: object = None
    debug: bool = False


@click.group("configs")
@click.pass_context
def configs(ctx):
    """
    Config commands.
    """
    db = ctx.obj.db
    debug = ctx.obj.debug
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
def add_config(ctx_obj, file, name, value):
    """Add an config to the database."""

    db = ctx_obj.db
    debug = ctx_obj.debug

    if not (name or file):
        console.exit_msg("A Name/Value pair or File must be provided")

    if file:
        config_data = json.load(file)
    else:
        config_data = {"name": name, "value": value}

    if debug:
        console.console.print_json(data={"config_data": config_data})

    crud.add_config(db, debug, config_data)


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

    db = ctx_obj.db
    debug = ctx_obj.debug

    if name:
        configs = crud.get_configs_by_match(db, name)
    else:
        configs = crud.get_configs(db)

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

    db = ctx_obj.db
    debug = ctx_obj.debug

    if not (config_name or file):
        console.exit_msg("A Name/Value pair or File must be provided")

    if file:
        config_data = json.load(file)
    else:
        config_data = {"name": config_name, "value": config_value}

    if not config_id:
        config = crud.get_config_by_match(db, config_data["name"])
        config_id = config.id
    else:
        config = crud.get_config(db, config_id)

    if config:
        if not config_value and config.value:
            config_data["value"] = config.value

    if debug:
        console.debug_msg(config_id)
        console.debug_msg(config_data)

    crud.update_config(db, debug, config_id, config_data)


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

    db = ctx_obj.db
    debug = ctx_obj.debug

    if config_name:
        config_id = crud.get_config_by_match(db, config_name).id

    if debug:
        console.console.print_json(data={"config_id": config_id})

    crud.delete_config(db, debug, config_id)


if __name__ == "__main__":
    configs()
