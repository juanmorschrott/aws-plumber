# UC-005 Dry-Run Mode

## Goal
The operator wants to verify what actions a tool would perform — including which AWS resources would be modified — without making any real changes to infrastructure.

## Actors
- Operator with valid AWS credentials
- Any tool that performs a write or modify operation against AWS (e.g. EBS disk upgrade, volume detach/attach)

## Problem
Tools that call destructive or irreversible AWS APIs (e.g. `ec2:ModifyVolume`, `ec2:DetachVolume`) in emergency scenarios carry a risk of acting on the wrong resource. There is no built-in confirmation that the operator selected the right instance or volume before the change is committed.

## Main Flow
1. The operator launches a tool with the `--dry-run` flag (e.g. `uv run aws-plumber upgrade-disk --dry-run`).
2. The tool runs the full interactive flow: credential validation, region selection, instance selection, volume selection, size input.
3. At every point where the tool would call a write AWS API, it instead prints a summary of the action that would be taken.
4. No AWS API write calls are made.
5. The tool exits with a message indicating it ran in dry-run mode and no changes were applied.

## Acceptance Criteria
- `--dry-run` flag is available on every tool that performs write operations.
- All read-only API calls (describe, list) execute normally in dry-run mode.
- Every skipped write operation is printed clearly, including resource IDs and parameters.
- The tool's exit code is 0 on successful dry-run.
- Dry-run mode is documented in the CLI help (`--help`).

## Implementation Notes

### Click integration
Pass `dry_run` as a Click option and thread it through the tool workflow:

```python
@main.command()
@click.option("--dry-run", is_flag=True, default=False, help="Simulate actions without making changes.")
def upgrade_disk(dry_run: bool):
    run_disk_upgrade(dry_run=dry_run)
```

### AWS client layer
Add a `dry_run: bool = False` parameter to every method that calls a write AWS API.
Since most boto3 write calls (e.g. `modify_volume`) do not support a native `DryRun` parameter,
the check is done before the API call:

```python
def modify_volume_size(self, volume_id: str, size: int, dry_run: bool = False) -> bool:
    if dry_run:
        print_info(f"[DRY-RUN] Would modify volume {volume_id} to {size}GB")
        return True
    # real API call below
    ...
```

### Tool workflow layer
The `dry_run` flag is passed down from the CLI entrypoint through the tool function
to every client method that performs a write. Read calls are unaffected.
