"""Main CLI entry point for AWS Plumber."""

import sys
import click
from . import __version__
from .ui.theme import display_banner
from .tools.menu import run_main_menu
from .tools.disk_upgrade import run_disk_upgrade
from .tools.waf_detection import run_waf_detection


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


@main.command(name="upgrade-disk")
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Simulate disk upgrade actions without making AWS changes.",
)
def upgrade_disk(dry_run: bool):
    """Run the EBS disk upgrade workflow, optionally in dry-run mode."""
    display_banner(__version__)
    run_disk_upgrade(dry_run=dry_run)


@main.command(name="detect-waf-blocking")
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Run detection in simulation mode (read-only; no AWS writes).",
)
def detect_waf_blocking(dry_run: bool):
    """Run WAF blocking detection, with optional dry-run flag support."""
    display_banner(__version__)
    run_waf_detection(dry_run=dry_run)


if __name__ == "__main__":
    main()
