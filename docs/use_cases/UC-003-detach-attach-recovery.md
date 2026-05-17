# UC-003 Detach/Attach Recovery

## Goal
The user wants to recover a failed disk upgrade by detaching and reattaching the affected volume using AWS control plane operations.

## Actors
- Operator with `awscliv2` installed and valid AWS credentials in `~/.aws/credentials`
- AWS instance with a volume attached that can be detached and reattached

## Main Flow
1. The tool detects a failed disk upgrade and offers the detach/attach recovery flow.
2. The tool displays the affected instance, volume, attachment, and availability zone.
3. The tool offers the operator the option to create a backup before any recovery operation: a snapshot of the affected volume and, when appropriate, an AMI or instance backup.
4. The tool requires explicit confirmation before proceeding with snapshot/backup and recovery operations.
5. The tool warns the operator that the recovery can require stopping the instance and may affect availability.
6. The operator confirms the detach/attach recovery flow.
7. The tool stops the instance if required for safe volume detachment.
7. The tool detaches the volume from the instance using AWS volume attachment APIs.
8. The tool reattaches the volume to the same or recovery instance as needed.
9. The tool starts the instance again if it was stopped during recovery.
10. The tool displays recovery results and status information.

## Acceptance Criteria
- Failed disk upgrades present a clear detach/attach recovery option.
- The recovery flow shows the instance, volume, attachment ID, and region/AZ.
- The tool offers a pre-operation backup and requires explicit confirmation before starting recovery.
- The backup option should include a volume snapshot and, if applicable, an AMI or instance-level backup.
- The operator receives a warning and must explicitly confirm before stopping or detaching the instance.
- The recovery flow works without relying on SSM or SSH access to the guest OS.
- The tool uses AWS volume operations and metadata rather than assuming filesystem details inside the instance.
- The operator can see success or failure info for the recovery steps.

## Notes
- The tool must treat the recovery path as an AWS control-plane operation, not an in-guest filesystem fix.
- Different operating systems and filesystem types must not be assumed; the tool should work from the volume attachment perspective.
- The recovery flow should assume SSM or SSH may be unavailable due to disk exhaustion.
- The tool must offer a pre-operation backup before any instance or volume operation, including volume snapshots and instance backup/AMI options.
- If the volume is root-backed and cannot be detached live, the tool should stop the instance first and then reattach before restarting.
- The tool should clearly separate the upgrade flow from the recovery flow so the operator understands the state changes being made.