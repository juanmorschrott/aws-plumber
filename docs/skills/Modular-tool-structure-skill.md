# Modular Tool Structure Skill

## Goal
Define the project structure and module layout so each CLI tool is easily recognizable, discoverable, and maintainable.

## Description
Each CLI tool should live in its own module or package, with a consistent naming convention and a clean entrypoint from the main CLI.
This makes the toolbox easier to extend and helps contributors find the implementation of each tool quickly.

## Requirements
- Each tool is implemented as a separate module or package.
- Tool modules use a consistent naming convention, such as `aws_plumber.tools.upgrade_disk` and `aws_plumber.tools.detect_waf_blocking`.
- The main CLI discovers or registers tools explicitly from a central command registry.
- Tool modules contain their own validation, AWS interaction, and user-facing prompts.
- The project structure should separate core CLI logic from individual tool implementations.

## Structure Guidance
- `aws_plumber/cli.py` or equivalent should contain the main menu and command dispatch logic.
- `aws_plumber/tools/` should contain one module per tool.
- Each tool module should export a clear entrypoint function and metadata for display name and description.
- Shared helpers and AWS utilities should live in a separate package or module, not inside individual tool modules.

## UX Expectations
- The main menu shows each tool with a recognizable name and short description.
- New tools can be added by creating a new module under the tools package and registering it once.
- Tool behavior is isolated so changes to one tool do not affect unrelated tools.

## AWS Client Patterns

- **Never use `resource.instances.all()` or equivalent unbounded collection calls.** Always pass server-side filters directly to the API call (e.g. `describe_instances(Filters=[...])`) to avoid fetching unnecessary resources and consuming API quota.
- **Region detection must respect boto3's resolution chain.** Do not force manual region selection if the user already has a region configured via `AWS_DEFAULT_REGION`, `AWS_PROFILE`, or `~/.aws/config`. Only prompt for region when `boto3.session.Session().region_name` returns `None`.

## Notes
- This skill is about project organization and maintainability, not the CLI appearance.
- A modular structure supports easier testing and incremental development.
- The command registry should make it simple to list available tools, even as the toolbox grows.