"""Main CLI entry point for AWS Plumber."""

import sys
import click
from . import __version__
from .ui.theme import display_banner
from .tools.menu import run_main_menu


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version=__version__)
def main(ctx):
    """AWS Plumber: Emergency and outage recovery automation for AWS."""
    if ctx.invoked_subcommand is None:
        # Default: show banner and run interactive menu
        display_banner(__version__)
        run_main_menu()


@main.command()
def interactive():
    """Launch the interactive CLI tool selection menu."""
    display_banner(__version__)
    run_main_menu()


if __name__ == "__main__":
    main()

