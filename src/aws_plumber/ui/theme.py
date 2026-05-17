"""UI theme and styling utilities with enhanced 8-bit aesthetic."""

from rich.console import Console
from rich.text import Text
from rich.style import Style
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# Enhanced color scheme: dark background with lemon-acid yellow accents
DARK_BG = "#1a1a1a"
ACCENT_COLOR = "#ccff00"    # Lemon-acid yellow accent
SECONDARY_ACCENT = "#ffcc00"  # AWS-inspired yellow (fallback)
GRAY_TEXT = "#c0c0c0"       # Neutral grayscale
SUCCESS_COLOR = "#00ff00"   # Bright green for success
ERROR_COLOR = "#ff0000"     # Bright red for errors
INFO_COLOR = "#0099ff"      # Cyan for info
WARN_COLOR = "#ffaa00"      # Orange for warnings


def display_banner(version: str) -> None:
    """Display the AWS Plumber banner with version."""
    banner = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                      🔧 AWS PLUMBER 🔧                         ║
    ║                  Emergency Recovery Automation                 ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style=Style(color=ACCENT_COLOR, bold=True))
    console.print(f"Version {version}", style=Style(color=GRAY_TEXT, dim=True))
    console.print()


def print_header(text: str) -> None:
    """Print a section header with styling."""
    console.print(f"\n[bold {ACCENT_COLOR}]{"─" * 60}[/]")
    console.print(f"[bold {ACCENT_COLOR}]{text}[/]")
    console.print(f"[bold {ACCENT_COLOR}]{"─" * 60}[/]\n")


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
    console.print(f"[bold {WARN_COLOR}]⚠ {text}[/]")


def create_bordered_panel(title: str, content: str, accent: str = ACCENT_COLOR) -> Panel:
    """Create a bordered panel with 8-bit styling."""
    return Panel(
        content,
        title=f"[bold {accent}]{title}[/]",
        border_style=accent,
        padding=(1, 2),
    )


def format_selection_menu(items: list[str], selected_index: int = 0) -> str:
    """Format a selection menu with highlighted current item."""
    lines = []
    for i, item in enumerate(items):
        if i == selected_index:
            lines.append(f"[bold {ACCENT_COLOR}]► {item}[/]")
        else:
            lines.append(f"  {item}")
    return "\n".join(lines)


def create_info_table(data: dict[str, str]) -> Table:
    """Create a styled info table."""
    table = Table(show_header=False, box=None, padding=(0, 1))
    for key, value in data.items():
        table.add_row(f"[bold {GRAY_TEXT}]{key}:[/]", f"[{ACCENT_COLOR}]{value}[/]")
    return table


def create_result_table(rows: list[dict[str, str]], headers: list[str]) -> Table:
    """Create a styled result table with headers."""
    table = Table(title="Results", show_header=True, header_style=f"bold {ACCENT_COLOR}")
    for header in headers:
        table.add_column(header)
    for row in rows:
        table.add_row(*[row.get(h, "") for h in headers])
    return table


def create_status_box(title: str, status: str, success: bool = True) -> Panel:
    """Create a status display box."""
    color = SUCCESS_COLOR if success else ERROR_COLOR
    symbol = "✓" if success else "✗"
    content = f"[bold {color}]{symbol} {status}[/]"
    return Panel(content, title=f"[bold {ACCENT_COLOR}]{title}[/]", border_style=ACCENT_COLOR)


def print_progress(message: str) -> None:
    """Print a progress indicator."""
    with Progress(
        SpinnerColumn(style=ACCENT_COLOR),
        TextColumn("[progress.description]{task.description}", style=GRAY_TEXT),
        console=console,
    ) as progress:
        progress.add_task(message, total=None)

