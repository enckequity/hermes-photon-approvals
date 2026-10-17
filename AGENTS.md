# Connector guardrails

Keep Hermes source unchanged. Use its supported approval transport and dashboard plugin APIs. No auto-approval, command execution, approval-policy changes, permanent grants or fallback allow. Every decision must bind to the original request and an authenticated configured approver. Keep customer state and credentials isolated per gateway. No secrets or private account identifiers in repository files, tests or logs. Run tests on DigitalOcean; do not install a runtime on the developer desktop. No GitHub Actions. Review security changes before release.
