"""EBS disk upgrade tool with recovery support."""

import sys
import time
from typing import Optional
from aws_plumber.aws import EC2Client
from aws_plumber.ui.theme import (
    print_header, print_success, print_error, print_info, print_warning,
    create_info_table, console, ACCENT_COLOR
)


def run_disk_upgrade(dry_run: bool = False) -> None:
    """Run the disk upgrade workflow."""
    print_header("EBS Disk Upgrade Tool")
    if dry_run:
        print_info("Dry-run mode enabled: write operations will be simulated.")

    # Initialize AWS client
    client = EC2Client()

    # Validate credentials
    if not client.validate_credentials():
        print_info("Please configure AWS credentials in ~/.aws/credentials or set environment variables")
        return

    # Get or set region
    if not client.region:
        region = select_region(client)
        if not region:
            print_error("Region selection cancelled")
            return
        client.set_region(region)
    else:
        client.set_region(client.region)

    # Select instance
    instance = select_instance(client)
    if not instance:
        print_error("Instance selection cancelled")
        return

    # Display instance details
    display_instance_details(instance)

    # Select volume
    volumes = client.get_instance_volumes(instance["id"])
    if not volumes:
        print_error(f"No volumes found attached to instance {instance['id']}")
        return

    volume = select_volume(volumes)
    if not volume:
        print_error("Volume selection cancelled")
        return

    # Get new disk size
    new_size = get_disk_size(volume["size"])
    if new_size is None or new_size <= volume["size"]:
        print_error("Invalid disk size. Size must be greater than current size")
        return

    # Attempt upgrade
    print_header("Starting Disk Upgrade")
    print_info(f"Upgrading volume {volume['id']} from {volume['size']}GB to {new_size}GB")

    if not client.modify_volume_size(volume["id"], new_size, dry_run=dry_run):
        print_error("Failed to initiate volume modification")
        return

    if dry_run:
        print_success("Dry-run completed successfully. No changes were applied.")
        display_upgrade_result(instance, volume, new_size)
        return

    # Wait for modification and check status
    if wait_for_volume_modification(client, volume["id"]):
        print_success(f"Volume {volume['id']} upgraded to {new_size}GB")
        display_upgrade_result(instance, volume, new_size)
    else:
        print_error("Volume modification failed or timed out")
        print_warning("\nDetach/Attach Recovery Available")
        offer_recovery(client, instance, volume, dry_run=dry_run)


def select_region(client: EC2Client) -> Optional[str]:
    """Select AWS region interactively."""
    print_info("Fetching available regions...")
    regions = client.get_regions()
    if not regions:
        return None

    console.print("\n[bold #ccff00]Select Region:[/]\n")
    for i, region in enumerate(regions[:10], 1):
        console.print(f"  {i}. {region}")

    if len(regions) > 10:
        console.print(f"  ... and {len(regions) - 10} more regions")

    try:
        choice = int(input("\nEnter region number: ").strip())
        if 1 <= choice <= len(regions):
            return regions[choice - 1]
    except (ValueError, IndexError):
        pass
    return None


def select_instance(client: EC2Client) -> Optional[dict]:
    """Select EC2 instance interactively."""
    print_info("Fetching instances...")
    instances = client.get_instances()
    if not instances:
        print_error("No instances found")
        return None

    console.print("\n[bold #ccff00]Select Instance:[/]\n")
    max_display = 10
    for i, inst in enumerate(instances[:max_display], 1):
        state_color = "#00ff00" if inst["state"] == "running" else "#ff9900"
        console.print(f"  {i}. {inst['name']:<20} {inst['id']:<20} [{state_color}]{inst['state']}[/]")

    if len(instances) > max_display:
        console.print(f"  ... and {len(instances) - max_display} more instances")

    try:
        choice = int(input("\nEnter instance number: ").strip())
        if 1 <= choice <= len(instances):
            return instances[choice - 1]
    except (ValueError, IndexError):
        pass
    return None


def select_volume(volumes: list[dict]) -> Optional[dict]:
    """Select volume interactively."""
    if len(volumes) == 1:
        return volumes[0]

    console.print("\n[bold #ccff00]Select Volume:[/]\n")
    for i, vol in enumerate(volumes, 1):
        console.print(f"  {i}. {vol['id']:<20} {vol['size']}GB {vol['type']:<10} ({vol['device']})")

    try:
        choice = int(input("\nEnter volume number: ").strip())
        if 1 <= choice <= len(volumes):
            return volumes[choice - 1]
    except (ValueError, IndexError):
        pass
    return None


def get_disk_size(current_size: int) -> Optional[int]:
    """Get new disk size from user."""
    console.print(f"\n[bold #ccff00]Current disk size: {current_size}GB[/]")
    try:
        new_size = int(input("Enter new disk size (GB): ").strip())
        return new_size if new_size > current_size else None
    except ValueError:
        return None


def display_instance_details(instance: dict) -> None:
    """Display instance information."""
    console.print("\n[bold #ccff00]Instance Details:[/]\n")
    details = {
        "Instance ID": instance["id"],
        "Name": instance["name"],
        "Type": instance["type"],
        "State": instance["state"],
        "Availability Zone": instance["az"],
    }
    console.print(create_info_table(details))


def wait_for_volume_modification(client: EC2Client, volume_id: str, timeout: int = 600) -> bool:
    """Wait for volume modification to complete."""
    print_info("Waiting for volume modification to complete (this may take several minutes)...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        mods = client.get_volume_modifications(volume_id)
        if mods:
            mod_state = mods[0]["ModificationState"]
            progress = mods[0].get("Progress", 0)
            console.print(f"  Status: {mod_state} ({progress}%)", end="\r")

            if mod_state == "completed":
                console.print()
                return True
            elif mod_state == "failed":
                console.print()
                return False

        time.sleep(10)

    console.print()
    return False


def display_upgrade_result(instance: dict, volume: dict, new_size: int) -> None:
    """Display successful upgrade results."""
    console.print("\n[bold #00ff00]Upgrade Complete![/]\n")
    result = {
        "Instance": instance["id"],
        "Volume": volume["id"],
        "New Size": f"{new_size}GB",
        "Status": "Successfully modified",
    }
    console.print(create_info_table(result))


def offer_recovery(client: EC2Client, instance: dict, volume: dict, dry_run: bool = False) -> None:
    """Offer detach/reattach recovery option."""
    console.print("\n[bold #ccff00]Recovery Options:[/]\n")
    console.print("The system can attempt to recover by detaching and reattaching the volume.")
    console.print("This may require stopping the instance.\n")

    confirm = input("[Y/n] Proceed with recovery? ").strip().lower()
    if confirm in ("y", ""):
        run_recovery(client, instance, volume, dry_run=dry_run)


def run_recovery(
    client: EC2Client, instance: dict, volume: dict, dry_run: bool = False
) -> None:
    """Execute detach/reattach recovery flow."""
    print_header("Detach/Attach Recovery")

    print_warning("⚠️  IMPORTANT WARNINGS:")
    print_warning("  • This operation may stop the instance and cause brief downtime")
    print_warning("  • The volume will be detached and reattached")
    print_warning("  • Ensure you have a backup before proceeding")

    confirm = input("\n[Y/n] Continue with recovery? ").strip().lower()
    if confirm not in ("y", ""):
        print_info("Recovery cancelled")
        return

    # Display recovery details
    console.print("\n[bold #ccff00]Recovery Details:[/]\n")
    recovery_info = {
        "Instance": instance["id"],
        "Instance State": instance["state"],
        "Volume": volume["id"],
        "Device": volume["device"],
        "Attachment ID": volume["attachment_id"],
        "Availability Zone": instance["az"],
    }
    console.print(create_info_table(recovery_info))

    # Stop instance if running
    if instance["state"] == "running":
        print_info("Stopping instance...")
        if client.stop_instance(instance["id"], dry_run=dry_run):
            if dry_run or client.wait_for_instance_stopped(instance["id"]):
                print_success("Instance stopped")
            else:
                print_error("Timeout waiting for instance to stop")
                return
        else:
            print_error("Failed to stop instance")
            return

    # Detach volume
    print_info("Detaching volume...")
    if client.detach_volume(volume["id"], instance["id"], dry_run=dry_run):
        if dry_run or client.wait_for_volume_available(volume["id"]):
            print_success("Volume detached")
        else:
            print_error("Timeout waiting for volume to detach")
            return
    else:
        print_error("Failed to detach volume")
        return

    # Reattach volume
    print_info("Reattaching volume...")
    if client.reattach_volume(
        volume["id"], instance["id"], volume["device"], dry_run=dry_run
    ):
        print_success("Volume reattached")
    else:
        print_error("Failed to reattach volume")
        return

    # Start instance if it was running
    if instance["state"] == "running":
        print_info("Starting instance...")
        if client.start_instance(instance["id"], dry_run=dry_run):
            if dry_run or client.wait_for_instance_running(instance["id"]):
                print_success("Instance started")
            else:
                print_error("Timeout waiting for instance to start")
                return
        else:
            print_error("Failed to start instance")
            return

    print_success("\n✓ Recovery completed successfully!")
    console.print("\n[bold #00ff00]Recovery Result:[/]\n")
    result = {
        "Instance": instance["id"],
        "Volume": volume["id"],
        "Status": "Recovered and operational",
        "Next Steps": "Monitor instance to verify disk is accessible",
    }
    console.print(create_info_table(result))
