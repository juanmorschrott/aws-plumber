# AWS Service Client Architecture Skill

## Goal
Define how AWS service clients are structured, named, and composed across the codebase.

## Description
Each AWS service has its own dedicated module and client class. Tools compose these clients directly without intermediate wrapper or aggregate client classes. This makes each module's scope explicit and keeps service concerns isolated.

## Module Layout

```
aws_plumber/aws/
├── __init__.py     # Public API: re-exports all service clients
├── ec2.py          # EC2Client — EC2/EBS operations, credentials, region management
├── waf.py          # WAFClient — WAF v2 operations
└── alb.py          # ALBClient — ALB/ELBv2 operations
```

## Conventions

- **One file, one service.** Each file maps to exactly one AWS service domain.
- **File naming:** lowercase service abbreviation (`ec2.py`, `waf.py`, `alb.py`).
- **Class naming:** `<Service>Client` (`EC2Client`, `WAFClient`, `ALBClient`).
- **No inheritance between service clients.** Service clients are independent; do not extend one from another.
- **EC2Client owns credentials and region management.** `validate_credentials()`, `get_regions()`, and `set_region()` live in `EC2Client` because they use EC2/STS endpoints internally. All other service clients accept `region: str` as a required constructor argument.
- **Public API via `__init__.py`.** All clients are re-exported from `aws/__init__.py`. Tools import from `..aws` rather than from individual service modules.

## Tool Composition Pattern

Tools instantiate only the service clients they need:

```python
# Example: a tool that requires EC2 + WAF
from ..aws import EC2Client, WAFClient

ec2_client = EC2Client()
ec2_client.validate_credentials()
region = select_region(ec2_client)   # uses ec2_client.get_regions()
waf_client = WAFClient(region=region)
```

Never create a composite or enhanced client class that wraps multiple services. Explicit instantiation in the tool makes dependencies visible and avoids unnecessary coupling.

## Adding a New Service Client

1. Create `aws_plumber/aws/<service>.py` with a single `<Service>Client` class.
2. The constructor must accept `region: str` as a required parameter and create the boto3 client there.
3. Do not add `set_region()` or session management to the new client; those belong in `EC2Client`.
4. Re-export the new client in `aws/__init__.py` (`__all__` list).
5. Add a corresponding test file `tests/test_<service>_client.py`.

## Notes

- This structure avoids the "god client" anti-pattern where a single class accumulates unrelated service methods.
- Adding or removing a service only touches one client file and its test; no other service client is affected.
- `ALBClient` is currently not consumed by any tool but is kept as part of the public API for future use.
