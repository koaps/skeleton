from rich import box
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

from skeleton.console import *

console = Console()


def get_content(config):
    """Extract text from configs dict."""
    title = "{}".format(config.ts)
    body = "{} = {}".format(config.name, config.value)
    return f"[b]{title}[/b]\n[yellow]{body}"


def display_configs(configs):
    if not isinstance(configs, list):
        configs = [configs]

    config_renderables = [Panel(get_content(config), expand=True) for config in configs]
    console.print(Columns(config_renderables))


def display_configs_minimal(configs):
    table = Table(title="[bold italic]Configs :speak_no_evil:[/]", box=box.SIMPLE)
    table.add_column("ID", style="bold", width=12, justify="center")
    table.add_column("Name")
    table.add_column("Value")
    table.add_column("TS")

    if not isinstance(configs, list):
        configs = [configs]

    for config in configs:
        table.add_row(
            str(config.id),
            config.name,
            config.value,
            str(config.ts),
        )

    console.print(table)
