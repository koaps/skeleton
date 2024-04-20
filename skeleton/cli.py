"""Skeleton CLI."""

from dataclasses import dataclass, field

import click

from skeleton import console, database
from skeleton.database import get_dsn

from skeleton.configs.commands import configs


@dataclass()
class RunCmd:
    debug: bool
    test: bool
    configs_db: str


@click.group("run")
@click.option("-d", "--debug", is_flag=True, default=False, help="Show debug outputs.")
@click.option("-t", "--test", is_flag=True, default=False, help="Use testing mode.")
@click.pass_context
def run(ctx, debug, test):
    """
    Skeleton - python cli template

    \b
    To manage configs, use `skeleton configs`

    For testing (fake data) use --test
    """
    data_dsn = get_dsn("configs", test)
    configs_db = next(database.get_db(debug, data_dsn))
    ctx.obj = RunCmd(debug, test, configs_db)
    if test or debug:
        console.test_msg("Using Test Databases")


run.add_command(configs)


if __name__ == "__main__":
    run()
