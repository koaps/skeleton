"""Skeleton CLI."""

from dataclasses import dataclass

import click

# import pprint

from skeleton import database
from skeleton.database import get_dsn

from skeleton.configs.commands import configs
from skeleton.configs import crud as configs_crud


@dataclass()
class RunCmd:
    config: object = None
    debug: bool = False
    db: object = None


@click.group("run")
@click.option("-c", "--config", default=None, help="Config name or config id.")
@click.option("-d", "--debug", is_flag=True, default=False, help="Show debug outputs.")
@click.pass_context
def run(ctx, config, debug):
    """
    Skeleton - python cli template

    \b
    To manage configs, use `skeleton configs`
    """
    data_dsn = get_dsn(debug, "configs")
    db = next(database.get_db(debug, data_dsn))

    if isinstance(config, int):
        _config = configs_crud.get_config(db, config)
    elif isinstance(config, str):
        _config = configs_crud.get_config_by_name(db, config)
    else:
        _config = None

    ctx.obj = RunCmd(_config, debug, db)


#    if debug:
#        pprint.pp(ctx.__dict__)


run.add_command(configs)


if __name__ == "__main__":
    run(auto_envvar_prefix="SKELETON")
