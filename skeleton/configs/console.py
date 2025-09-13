from rich import box
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

from skeleton.console import *

console = Console()


def display_configs(configs):
    table = Table(title="[bold italic]Configs[/]")
    table.add_column("ID", style="bold", width=12, justify="center")
    table.add_column("Name", justify="center")
    table.add_column("Value")

    if not isinstance(configs, list):
        configs = [configs]

    for config in configs:
        table.add_row(
            str(config.id),
            config.name,
            config.value,
        )

    console.print(table)


def display_configs_minimal(configs):
    table = Table(title="[bold italic]Configs :speak_no_evil:[/]", box=box.SIMPLE)
    table.add_column("ID", style="bold", width=12, justify="center")
    table.add_column("Name")
    table.add_column("Value")

    if not isinstance(configs, list):
        configs = [configs]

    for config in configs:
        table.add_row(
            str(config.id),
            config.name,
            config.value,
        )

    console.print(table)
