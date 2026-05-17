"""Main menu and tool selection interface."""

import sys
from .disk_upgrade import run_disk_upgrade
from ..ui.theme import print_header, console


def run_main_menu() -> None:
    """Display main menu and handle tool selection."""
    tools = [
        {"name": "Upgrade EBS Disk", "description": "Upgrade instance EBS disk with recovery support", "handler": run_disk_upgrade},
        {"name": "Exit", "description": "Exit the CLI", "handler": None},
    ]

    print_header("AWS Plumber - Tool Selection")
    console.print("\nAvailable Tools:\n")

    while True:
        # Display menu
        for i, tool in enumerate(tools, 1):
            console.print(f"  {i}. {tool['name']}")
            console.print(f"     {tool['description']}\n")

        try:
            choice = input("Select tool (number) or Q to quit: ").strip().lower()
            if choice == "q":
                console.print("[dim]Exiting AWS Plumber.[/]")
                sys.exit(0)

            idx = int(choice) - 1
            if 0 <= idx < len(tools):
                selected_tool = tools[idx]
                if selected_tool["handler"] is None:
                    console.print("[dim]Exiting AWS Plumber.[/]")
                    sys.exit(0)
                console.clear()
                selected_tool["handler"]()
                return
            else:
                console.print("[bold #ff0000]Invalid selection. Please try again.[/]\n")
        except ValueError:
            console.print("[bold #ff0000]Invalid input. Please enter a number or Q.[/]\n")

