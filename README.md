# AWS Plumber 🔧

AWS Plumber is an open source Python 3.12 CLI toolbox for automating emergency and outage recovery workflows on AWS.

The project is designed to help operators recover infrastructure quickly, safely, and consistently. Tools include EBS disk upgrades, recovery flows, and security diagnostics.

## Key Features

- Lightweight interactive CLI for outage response and infrastructure recovery.
- **Upgrade EBS Disk**: Automated EBS disk upgrade with detach/attach recovery support.
- **Detect WAF Blocking**: Analyze AWS WAF blocking events and identify problematic rules.
- Control-plane recovery flows for detach and reattach operations.

## Getting Started

### Prerequisites

- Python 3.12
- `awscliv2` installed and configured
- Valid AWS credentials in `~/.aws/credentials`

### Installation

```bash
cd aws-plumber
uv sync
```

### Usage

```bash
uv run aws-plumber
```

Navigate tools with **↑/↓ arrow keys**, select with **Enter**, or use **numbers** for direct selection.

## Project Structure

```
aws_plumber/
├── aws/                      # AWS service clients (one file per service)
│   ├── __init__.py          # Public API: EC2Client, WAFClient, ALBClient
│   ├── ec2.py               # EC2Client: EC2/EBS operations, credentials, region management
│   ├── waf.py               # WAFClient: WAF v2 log analysis and Web ACL queries
│   └── alb.py               # ALBClient: ALB/ELBv2 operations
├── tools/                    # Tool implementations
│   ├── registry.py          # Tool registry system
│   ├── menu.py              # Interactive tool selection menu
│   ├── disk_upgrade.py      # EBS disk upgrade tool (UC-002)
│   └── waf_detection.py     # WAF blocking detection tool (UC-004)
├── ui/
│   ├── __init__.py
│   └── theme.py             # Styling & UI components
├── cli.py                   # CLI entry point
└── __init__.py
```

## Available Tools

1. **Upgrade EBS Disk** – Instance selection, volume upgrade, automatic recovery
2. **Detect WAF Blocking** – WAF scope selection, logging check, event analysis

## Dependencies

- boto3 >=1.43.9 – AWS SDK
- click >=8.4.0 – CLI framework
- rich >=15.0.0 – Terminal styling
- readchar >=4.2.2 – Interactive keyboard input

## IAM Permissions

The following minimum IAM permissions are required:

| Tool | Actions required |
|---|---|
| Upgrade EBS Disk | `ec2:DescribeRegions` `ec2:DescribeInstances` `ec2:DescribeVolumes` `ec2:DescribeVolumesModifications` `ec2:ModifyVolume` `ec2:DetachVolume` `ec2:AttachVolume` |
| Detect WAF Blocking | `wafv2:ListWebACLs` `wafv2:GetLoggingConfiguration` `logs:FilterLogEvents` |

## Documentation

- `docs/use_cases/` – user-facing scenarios and acceptance criteria
- `docs/skills/` – CLI appearance and aesthetic guidelines

## License

This project is licensed under the [MIT License](LICENSE).