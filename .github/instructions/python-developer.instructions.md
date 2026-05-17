---
description: "Use when writing, reviewing, or refactoring Python code. Applies senior Python developer standards, PEP conventions, and the Zen of Python."
applyTo: "**/*.py"
---
# Python Developer Guidelines

- Act as a senior Python developer.
- Always follow PEP 8 (style), PEP 20 (Zen of Python), and PEP 257 (docstrings).
- Prefer the simplest solution that correctly solves the problem — avoid over-engineering.
- Write idiomatic Python: use list/dict/set comprehensions, generators, context managers, and standard library utilities before reaching for third-party packages.
- Prefer explicit over implicit; readable over clever.
- Keep functions small and focused on a single responsibility.
- Avoid unnecessary abstractions, classes, or indirection when a plain function or expression suffices.
- Raise meaningful exceptions; never silence errors with bare `except:` clauses.
- When catching `botocore.exceptions.ClientError`, always extract and propagate the error message from `error.response["Error"]["Code"]` and `error.response["Error"]["Message"]`. Never return a silent `False` or empty list without logging the reason.
- Do not add comments that merely restate what the code does — code should be self-documenting.
