# UC-002 Run Disk Upgrade

## Goal
The user wants to upgrade an instance EBS disk from the CLI and recover with detach/attach if the upgrade fails.

## Actors
- Operator with `awscliv2` installed and valid AWS credentials in `~/.aws/credentials`
- AWS instance with an attachable EBS volume

## Main Flow
1. User selects `upgrade-disk-tool` from the main CLI display.
2. The tool validates AWS credentials and checks whether a default region is configured.
3. If no region is configured, the user is prompted to choose a region.
4. The tool redirects to the `upgrade-disk-tool` screen.
5. The user navigates the instance list using the up/down arrow keys and selects an instance with Enter.
6. The CLI displays basic instance details and prompts for a new disk size.
7. The tool offers the operator the option to create a backup before any modification: a snapshot of the affected volume and, when appropriate, an AMI or instance backup.
8. The tool requires explicit confirmation before proceeding with snapshot/backup and disk upgrade operations.
9. The user enters a disk upgrade size greater than the current disk size.
10. The tool validates the requested size and attempts the disk upgrade.
11. If the upgrade succeeds, the tool displays the result information.
12. If the upgrade fails, the tool proposes executing the detach/attach recovery flow and shows the data required for that operation.
13. If detach/attach recovery works, the tool displays recovery result information.

## Acceptance Criteria
- The `upgrade-disk-tool` screen appears after selecting the disk upgrade tool.
- The tool validates AWS credentials and prompts for region selection only if needed.
- The tool offers a pre-operation backup and requires explicit confirmation before modifying the instance or volume.
- The backup option should include a volume snapshot and, if applicable, an AMI or instance-level backup.
- The instance list is navigable with up/down arrows and supports selecting an instance with Enter.
- The selected instance details are shown before entering a new disk size.
- The disk size prompt requires a value greater than the current size.
- Successful upgrades show result information.
- Failed upgrades offer a detach/attach recovery option with required operation details.
- Successful detach/attach recovery shows result information.

## Notes
- The list display should show a maximum of 10 instances at once, but all instances must be selectable.
- The upgrade tool must validate the requested disk size before attempting the operation.
- The tool must offer a pre-operation backup before any instance or volume operation, including volume snapshots and instance backup/AMI options.
- Recovery data should include the volume, instance, and attachment details needed to detach and reattach the volume.
- The tool flow must account for cases where SSM or SSH access is unavailable due to disk exhaustion; recovery should use AWS volume operations rather than relying on in-guest commands.
- Detach/attach recovery should explicitly warn the operator and require confirmation before stopping, detaching, or modifying the instance state.
- The tool should avoid assumptions about the guest filesystem and use discovery data from the volume and instance attachment metadata.