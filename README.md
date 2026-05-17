# AWS Plumber

AWS Plumber is an open source Python 3.12 CLI toolbox for automating emergency and outage recovery workflows on AWS.

The project is designed to help operators recover infrastructure quickly, safely, and consistently. The first tool in the toolbox automates EBS disk upgrades and includes recovery flows for detach/attach operations when disk modifications fail.

## Key Features

- Lightweight CLI for outage response and infrastructure recovery.
- First tool: automated EBS disk upgrade with recovery support.
- Control-plane recovery flows for detach and reattach operations.
- AWS region selection when configuration is unavailable.
- Backup-first workflow with snapshot or instance backup confirmation.

## Getting Started

### Prerequisites

- Python 3.12
- `awscliv2` installed and configured
- Valid AWS credentials in `~/.aws/credentials`
- `pyproject.toml` for dependency management

### Installation

1. Clone the repository.
2. Create and activate a Python 3.12 virtual environment.
3. Install dependencies from `pyproject.toml`.

### Usage

Run the CLI from the project root:

```bash
aws-plumber
```

The initial experience includes a main menu with the available operational tools.

## Project Structure

- `README.md` – project overview and getting started guide
- `docs/use_cases/` – user-facing scenarios and acceptance criteria
- `docs/skills/` – design guidance for CLI behavior and aesthetic
- `.github/instructions/` – developer and code-style guidance

## Documentation

- `docs/use_cases/UC-001-run-cli-app.md` – main CLI launch and tool selection flow
- `docs/use_cases/UC-002-run-disk-upgrade.md` – disk upgrade flow with region selection and recovery
- `docs/use_cases/UC-003-detach-attach-recovery.md` – detach/attach recovery flow with backup confirmation

## Contributing

Contributions are welcome. Suggested next steps:

- Review the use cases and skills in `docs/`
- Implement the CLI flow and tool behavior
- Add tests for the upgrade and recovery workflows

## License

This project is intended to be open source and can be licensed appropriately by the maintainers.