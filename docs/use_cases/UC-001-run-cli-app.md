# UC-001 Run CLI App

## Goal
The user wants to launch the AWS Plumber CLI and see the available emergency tools.

## Actors
- Operator with `awscliv2` installed and configured with a valid AWS profile

## Main Flow
1. User opens a terminal
2. User executes `aws-plumber`
3. The application displays a banner with the version and the list of available tools
4. The user navigates the tool list using up/down arrows and selects a tool with Enter
5. The selected tool name is shown on the left and its description is displayed on the right

## Acceptance Criteria
- `aws-plumber` displays a banner with the application version
- `aws-plumber` displays the list of available tools in an interactive menu
- The main menu supports up/down arrow navigation and Enter selection
- Selected tool name and description are visible in the UI
- The initial tool shown is EBS disk upgrade with recovery support

## Notes
- The first tool is an EBS disk upgrade workflow that can also run detach/attach recovery when an upgrade error occurs
- Dependencies are managed via `pyproject.toml`