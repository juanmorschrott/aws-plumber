# UC-004 Detect WAF Blocking

## Goal
The user wants to detect if AWS WAF is blocking requests to a service and identify the rule or rule group responsible.

## Actors
- Operator with `awscliv2` installed and valid AWS credentials in `~/.aws/credentials`
- AWS WAF resources configured for the target service

## Main Flow
1. User selects `detect-waf-blocking` from the main CLI display.
2. The tool validates AWS credentials and checks whether a default region is configured.
3. If no region is configured, the user is prompted to choose a region.
4. The tool redirects to the WAF diagnostics screen.
5. The user selects the WAF scope or service resource to inspect (regional WAF, CloudFront, ALB, or API Gateway).
6. The tool checks whether WAF logging is enabled and whether it can access recent blocking events.
7. If logging is unavailable, the tool informs the operator and provides guidance on how to enable WAF logs.
8. If blocking events are available, the tool displays a simplified list of blocked requests, including URL/path, rule name, rule group, and action.
9. The tool summarizes the most impactful blocks and highlights the rules causing the most blocked requests.
10. The operator can review the findings and use them to diagnose whether WAF is the source of the outage.

## Acceptance Criteria
- The `detect-waf-blocking` tool is available from the main CLI menu.
- The tool validates AWS credentials and prompts for region selection only if needed.
- The tool allows selection of WAF scope or target resource.
- The tool checks whether WAF logging is enabled and reports if no block data is available.
- The tool displays a simplified list of blocked requests with URL/path, rule name, rule group, and action.
- The tool summarizes the top blocked rules and helps identify whether WAF is causing the service issue.

## Notes
- This tool is a diagnostic flow, not a remediation flow.
- The tool should avoid assuming the exact request body or payload; it should focus on blocking events and metadata.
- If WAF logs are not enabled, the tool should still provide clear guidance on the missing visibility.
- The UI should keep the output concise and highlight the most relevant block rules.