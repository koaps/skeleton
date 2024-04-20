import json
import sys

from rich.console import Console

console = Console()


def debug_msg(msg):
    console.print(f":mag_right: [bold light_slate_grey]Debug:[/] {msg}")


def exit_msg(msg):
    console.print(f":disappointed: {msg}")
    sys.exit(1)


def fail_msg(msg):
    console.print(f":red_circle: [bold red]Failed:[/] {msg}")


def info_msg(msg):
    console.print(f":blue_circle: [bold blue]Info:[/] {msg}")


def json_msg(msg):
    console.print(json.dumps(str(msg)))


def ok_msg(msg):
    console.print(f":green_circle: [bold green]Success:[/] {msg}")


def raw_msg(msg):
    console.print(msg)


def test_msg(*args):
    if args.__len__() > 1:
        console.print(f":yellow_circle: [yellow]{args[0]}[/]", end=None)
        console.print(args[1:])
    else:
        console.print(f":yellow_circle: [yellow]{args[0]}[/]")


def trace_error():
    console.print_exception(extra_lines=8, show_locals=True)


def warn_msg(msg):
    console.print(f":orange_circle: [bold rgb(255,165,0)]Warning:[/] {msg}")
