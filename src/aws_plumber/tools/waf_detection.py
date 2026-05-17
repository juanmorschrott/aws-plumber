"""WAF blocking detection tool for identifying WAF-blocked requests."""

from typing import Optional
from aws_plumber.aws import EC2Client, WAFClient
from aws_plumber.ui.theme import (
    print_header, print_success, print_error, print_info, print_warning,
    create_info_table, console, ACCENT_COLOR, create_result_table
)


def run_waf_detection(dry_run: bool = False) -> None:
    """Run the WAF blocking detection workflow."""
    print_header("WAF Blocking Detection Tool")
    if dry_run:
        print_info("Dry-run mode enabled: this tool is read-only and will not modify AWS resources.")

    ec2_client = EC2Client()

    if not ec2_client.validate_credentials():
        print_info("Please configure AWS credentials in ~/.aws/credentials or set environment variables")
        return

    if not ec2_client.region:
        region = select_region(ec2_client)
        if not region:
            print_error("Region selection cancelled")
            return
    else:
        region = ec2_client.region

    waf_client = WAFClient(region=region)

    # Select WAF scope
    scope = select_waf_scope()
    if not scope:
        print_error("Scope selection cancelled")
        return

    # Get WAF Web ACLs
    print_info("Fetching WAF Web ACLs...")
    web_acls = waf_client.list_waf_resources(scope)

    if not web_acls:
        print_error(f"No WAF Web ACLs found in {scope} scope")
        return

    # Select Web ACL
    web_acl = select_web_acl(web_acls)
    if not web_acl:
        print_error("Web ACL selection cancelled")
        return

    # Check logging configuration
    print_info("Checking WAF logging configuration...")
    logs_config = waf_client.get_waf_logs_config(web_acl["ARN"])

    if not logs_config:
        print_warning("WAF logging is not enabled")
        print_info("\nTo enable WAF logging:")
        print_info("  1. Go to AWS WAF console")
        print_info("  2. Select your Web ACL")
        print_info("  3. Enable logging to CloudWatch Logs")
        return

    # Get log group name
    log_group_name = logs_config.get("LogDestinationConfigs", [None])[0]
    if not log_group_name:
        print_error("Could not determine WAF log group")
        return

    # Extract log group name from ARN
    log_group_name = log_group_name.split(":")[-1]

    print_success(f"WAF logging enabled: {log_group_name}")

    # Display Web ACL details
    display_waf_details(web_acl, logs_config)

    # Get blocking events
    print_info("Analyzing recent blocking events (last 15 minutes)...")
    blocking_events = waf_client.get_recent_blocking_events(log_group_name, minutes=15)

    if not blocking_events:
        print_info("No blocking events found in the last 15 minutes")
        return

    # Display results
    display_blocking_events(blocking_events)


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


def select_waf_scope() -> Optional[str]:
    """Select WAF scope interactively."""
    scopes = [
        {"name": "Regional WAF", "value": "REGIONAL"},
        {"name": "CloudFront Distribution", "value": "CLOUDFRONT"},
    ]

    console.print("\n[bold #ccff00]Select WAF Scope:[/]\n")
    for i, scope in enumerate(scopes, 1):
        console.print(f"  {i}. {scope['name']}")

    try:
        choice = int(input("\nEnter scope number: ").strip())
        if 1 <= choice <= len(scopes):
            return scopes[choice - 1]["value"]
    except (ValueError, IndexError):
        pass
    return None


def select_web_acl(web_acls: list[dict]) -> Optional[dict]:
    """Select Web ACL interactively."""
    if not web_acls:
        return None

    if len(web_acls) == 1:
        return web_acls[0]

    console.print("\n[bold #ccff00]Select Web ACL:[/]\n")
    for i, acl in enumerate(web_acls[:10], 1):
        console.print(f"  {i}. {acl['Name']}")

    if len(web_acls) > 10:
        console.print(f"  ... and {len(web_acls) - 10} more Web ACLs")

    try:
        choice = int(input("\nEnter Web ACL number: ").strip())
        if 1 <= choice <= len(web_acls):
            return web_acls[choice - 1]
    except (ValueError, IndexError):
        pass
    return None


def display_waf_details(web_acl: dict, logs_config: dict) -> None:
    """Display WAF Web ACL details."""
    console.print("\n[bold #ccff00]Web ACL Details:[/]\n")
    details = {
        "Web ACL Name": web_acl["Name"],
        "ARN": web_acl["ARN"],
        "Capacity": str(web_acl.get("Capacity", "N/A")),
        "Logging Enabled": "Yes",
    }
    console.print(create_info_table(details))


def display_blocking_events(blocking_events: list[dict]) -> None:
    """Display blocking events summary."""
    console.print("\n[bold #ccff00]Recent Blocking Events (Last 15 Minutes):[/]\n")

    if not blocking_events:
        print_info("No blocking events detected")
        return

    # Prepare table data
    rows = []
    total_blocks = 0
    for event in blocking_events[:10]:
        block_count = event.get("block_count", "1")
        rule_id = event.get("terminatingRuleId", "N/A")
        rule_group = event.get("ruleGroupList", "N/A")

        rows.append(
            {
                "Rule ID": rule_id,
                "Rule Group": rule_group,
                "Block Count": block_count,
            }
        )

        try:
            total_blocks += int(block_count)
        except (ValueError, TypeError):
            total_blocks += 1

    # Display table
    if rows:
        table = create_result_table(rows, ["Rule ID", "Rule Group", "Block Count"])
        console.print(table)

    # Display summary
    console.print("\n[bold #ccff00]Summary:[/]\n")
    summary = {
        "Total Blocking Events": str(total_blocks),
        "Unique Rules Triggered": str(len(blocking_events)),
        "Time Range": "Last 15 minutes",
        "Status": "Review blocking rules if service is impacted" if total_blocks > 0 else "No issues detected",
    }
    console.print(create_info_table(summary))

    if total_blocks > 0:
        print_warning("\nIf your service is experiencing issues, review the rules above")
        print_info("Consider adjusting WAF rules to allow legitimate traffic")
