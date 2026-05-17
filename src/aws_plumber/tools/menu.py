"""Main menu and tool selection interface with tool registry."""

import sys
import readchar
from .registry import get_registry
from .disk_upgrade import run_disk_upgrade
from .waf_detection import run_waf_detection
from aws_plumber.ui.theme import print_header, console, ACCENT_COLOR


def initialize_tools() -> None:
    """Initialize all available tools in the registry."""
    registry = get_registry()

    registry.register(
        name="Upgrade EBS Disk",
        description="Upgrade instance EBS disk with recovery support",
        handler=run_disk_upgrade,
        category="Storage",
    )

    registry.register(
        name="Detect WAF Blocking",
        description="Identify if AWS WAF is blocking requests",
        handler=run_waf_detection,
        category="Security",
    )


def run_main_menu() -> None:
    """Display main menu and handle tool selection with arrow keys."""
    registry = get_registry()
    if not registry.get_tools():
        initialize_tools()

    tools = registry.get_tools()
    selected_idx = 0

    while True:
        console.clear()
        print_header("Available Tools")
        
        # Display tools with selection indicator
        for i, tool in enumerate(tools):
            if i == selected_idx:
                indicator = f"[bold {ACCENT_COLOR}]►[/]"
            else:
                indicator = " "
            
            status = "[bold #00ff00]✓[/]"
            console.print(f"{indicator} {status} {tool.name}")
            console.print(f"   {tool.description}\n")

        console.print(f"[dim]↑↓ Navigate | Enter Select | Q Quit[/]\n")

        try:
            char = readchar.readchar()
            
            # Handle arrow keys
            if char == "\x1b":  # Escape sequence
                next_char = readchar.readchar()
                if next_char == "[":
                    arrow = readchar.readchar()
                    if arrow == "A":  # Up arrow
                        selected_idx = (selected_idx - 1) % len(tools)
                    elif arrow == "B":  # Down arrow
                        selected_idx = (selected_idx + 1) % len(tools)
            
            # Handle enter/return
            elif char in ("\r", "\n"):
                break
            
            # Handle q for quit
            elif char.lower() == "q":
                console.print("[dim]Exiting AWS Plumber.[/]")
                sys.exit(0)
            
            # Handle numbers 1-9
            elif char.isdigit():
                idx = int(char) - 1
                if 0 <= idx < len(tools):
                    selected_idx = idx
                    break
                    
        except (KeyboardInterrupt, EOFError):
            console.print("[dim]Exiting AWS Plumber.[/]")
            sys.exit(0)

    # Execute selected tool
    selected_tool = tools[selected_idx]
    console.clear()
    
    try:
        selected_tool.handler()
    except KeyboardInterrupt:
        console.print("\n[dim]Operation cancelled by user.[/]")
    except Exception as e:
        console.print(f"\n[bold #ff0000]Error: {str(e)}[/]")




