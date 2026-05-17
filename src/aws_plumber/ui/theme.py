"""UI theme and styling utilities."""

from rich.console import Console
from rich.text import Text
from rich.style import Style
from rich.panel import Panel
from rich.table import Table

console = Console()

# Color scheme: dark background with yellow accents (AWS orange/yellow)
DARK_BG = "#1a1a1a"
YELLOW_ACCENT = "#ffcc00"  # AWS-inspired yellow
GRAY_TEXT = "#c0c0c0"      # Neutral grayscale
SUCCESS_COLOR = "#00ff00"  # Bright green for success
ERROR_COLOR = "#ff0000"    # Bright red for errors
INFO_COLOR = "#0099ff"     # Cyan for info


def display_banner(version: str) -> None:
    """Display the AWS Plumber banner with version."""
    banner = """
╔════════════════════════════════════════════════════════════════╗
║                     🔧 AWS PLUMBER 🔧                         ║
║                  Emergency Recovery Automation                 ║
╚════════════════════════════════════════════════════════════════╝
"""
    console.print(banner, style=Style(color=YELLOW_ACCENT, bold=True))
    console.print(f"Version {version}", style=Style(color=GRAY_TEXT, dim=True))
    console.print()


def print_header(text: str) -> None:
    """Print a section header with styling."""
    console.print(f"\n[bold {YELLOW_ACCENT}]{"─" * 60}[/]")
    console.print(f"[bold {YELLOW_ACCENT}]{text}[/]")
    console.print(f"[bold {YELLOW_ACCENT}]{"─" * 60}[/]\n")


def print_success(text: str) -> None:
    """Print a success message."""
    console.print(f"[bold {SUCCESS_COLOR}]✓ {text}[/]")


def print_error(text: str) -> None:
    """Print an error message."""
    console.print(f"[bold {ERROR_COLOR}]✗ {text}[/]")


def print_info(text: str) -> None:
    """Print an info message."""
    console.print(f"[{INFO_COLOR}]ℹ {text}[/]")


def print_warning(text: str) -> None:
    """Print a warning message."""
    console.print(f"[bold {YELLOW_ACCENT}]⚠ {text}[/]")


def create_bordered_panel(title: str, content: str) -> Panel:
    """Create a bordered panel with 8-bit styling."""
    return Panel(
        content,
        title=f"[bold {YELLOW_ACCENT}]{title}[/]",
        border_style=YELLOW_ACCENT,
        padding=(1, 2),
    )


def format_selection_menu(items: list[str], selected_index: int = 0) -> str:
    """Format a selection menu with highlighted current item."""
    lines = []
    for i, item in enumerate(items):
        if i == selected_index:
            lines.append(f"[bold {YELLOW_ACCENT}]► {item}[/]")
        else:
            lines.append(f"  {item}")
    return "\n".join(lines)


def create_info_table(data: dict[str, str]) -> Table:
    """Create a styled info table."""
    table = Table(show_header=False, box=None, padding=(0, 1))
    for key, value in data.items():
        table.add_row(f"[bold {GRAY_TEXT}]{key}:[/]", f"[{YELLOW_ACCENT}]{value}[/]")
    return table

