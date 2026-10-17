# Hermes Photon approval cards

Approve a specific Hermes command once, or deny it, from an authenticated workspace opened inside Messages. This standalone plugin uses Hermes's approval transport and dashboard plugin APIs. Hermes source stays unchanged and Hermes keeps final authority over execution.

**Status: experimental.** Automated contract tests run against Hermes v0.22.2 on DigitalOcean. Live authenticated phone approval is not yet qualified. The earlier multi-select poll is not used by this connector. The first release uses Spectrum's existing shared-line API, not Photon 2 beta projects.

## What happens

1. Hermes determines that a command needs approval and gives this plugin a redacted, request-bound prompt.
2. The plugin sends one Spectrum card to the operator-configured existing DM. Its URL contains a request ID, not a credential.
3. Opening the card loads the native Hermes dashboard plugin and its existing login. The API checks the configured provider, user and organization.
4. Approve once or Deny records one atomic decision. Hermes validates its request ID, digest, allowed scope and timeout before continuing.

An old card cannot approve a later request. Multiple clicks have one winner. Missing identity, expiry, invalid choices and delivery failures deny. A recorded decision is not proof that a command executed. A host interruption or timeout can discard a late response. Reopen the card to refresh state; consult the original conversation for execution results.

## Requirements

- Unmodified Hermes with `register_approval_transport` and native dashboard plugins. Tested revision: `d923a5eb487a17c0a68801bba9ef0f56c81040a8` (v0.22.2). Other versions need qualification.
- One isolated gateway/container and private home per tenant. Profiles alone are not tenant isolation. Gateway and dashboard must share this tenant's private state directory.
- Existing authenticated HTTPS dashboard origin reachable from the recipient's device. The plugin refuses an ungated dashboard. It does not expose a private dashboard or create an authentication service.
- Trusted in-process plugin execution. Do not loosen a shared host's isolation policy to install it.
- An existing Spectrum shared-line project and designated E.164 DM, plus the Spectrum Messages extension for in-Messages rendering. Groups and dedicated lines are not supported in this release.
- Maintained `grpcurl` 1.9.4 and official `@photon-ai/advanced-imessage` 2.3.0 proto schemas. These are runtime prerequisites, not vendored code. Verify publisher checksums/integrity before installation.

## Install on the gateway

Use a reviewed release or full commit SHA. Run these steps in the runtime's own environment, not on a developer desktop. This repository ships a full Hermes directory plugin **and** a Python library; installing the wheel alone does not install dashboard assets or `plugin.yaml`.

```sh
# Set APPROVAL_REVISION to the reviewed full commit SHA first.
git clone https://github.com/enckequity/hermes-photon-approvals \
  "$HERMES_HOME/plugins/photon-approvals"
git -C "$HERMES_HOME/plugins/photon-approvals" checkout --detach "$APPROVAL_REVISION"
# Use Hermes's actual Python environment; preserve its pinned dependencies.
uv pip install --python /path/to/hermes/python --no-deps \
  "$HERMES_HOME/plugins/photon-approvals"
hermes plugins validate "$HERMES_HOME/plugins/photon-approvals"
```

Installation and enabling are distinct. Keep the transport set to `builtin` until configuration and authenticated access pass. Do not install arbitrary latest code into production.

Set these variables through your existing runtime secret/config manager for both gateway and dashboard:

```dotenv
PHOTON_APPROVAL_TENANT_ID=your-isolated-tenant-id
PHOTON_APPROVAL_PUBLIC_URL=https://your-authenticated-agent.example
PHOTON_APPROVAL_PROVIDER=your-native-auth-provider-id
PHOTON_APPROVAL_USER_ID=your-verified-stable-user-id
PHOTON_APPROVAL_ORG_ID=your-verified-org-id
PHOTON_APPROVAL_DM=+15555550123
PHOTON_APPROVAL_STATE_DIR=/private/hermes-home/photon-approvals
PHOTON_APPROVAL_GRPCURL=/absolute/path/to/grpcurl
PHOTON_APPROVAL_PROTO_DIR=/absolute/path/to/advanced-imessage/2.3.0/proto
# Existing runtime credentials, supplied by your secret manager:
PHOTON_PROJECT_ID=your-existing-spectrum-project-id
PHOTON_PROJECT_SECRET=your-existing-spectrum-project-secret
```

The public URL must be the exact HTTPS origin used by the authenticated dashboard, with no path, query or credentials. The org ID may be empty only when the verified provider has no organization. Obtain the identity from verified native session evidence, never a guessed email address. Do not copy an owner's Photon credentials into customer gateways. The DM and identity are operator configuration, never model arguments.

After native discovery, authenticated route checks and device qualification, explicitly enable and select the transport:

```yaml
plugins:
  enabled: [photon-approvals] # retain your other enabled entries
security:
  approval:
    transport: photon-cards
    transport_fallback: deny
```

The transport does not change `approvals.mode`. Hermes still decides which actions need approval. Restart gateway/dashboard using your normal supervisor after configuration changes. Verify the plugin's native `/photon-approvals` page and a harmless approval request before production use.

## Recovery and operations

Restore `security.approval.transport: builtin` to use stock controls. Do not remove or replace state while a request is pending. No session or permanent grant is offered. Timeouts are capped at 300 seconds and remain bounded by Hermes's own timeout.

The state directory must be owned by the runtime user with mode 0700; the SQLite database is 0600. It stores redacted display text, identity scope, decision and non-credential card receipts. Keep it inside the tenant's trusted gateway boundary, away from untrusted execution environments. It is not a separate protection against code that can already edit that user's database or Hermes configuration. It never stores Photon tokens or project secrets.

A private intent is written before sending. Do not automatically retry an uncertain send: inspect its receipt and provider state first. Bubble updates are best effort and may be skipped near the deadline; the authenticated page reads canonical state. Retain the private state only as long as your audit policy requires. Remove it only after all pending requests have ended and the plugin is disabled.

## Tests

Run in the target Hermes environment with its dependencies activated:

```sh
python -m unittest discover -s tests -v
node --check dashboard/dist/index.js
node --test tests/frontend.test.cjs
```

Tests use synthetic identities and temporary databases. Photon network calls are mocked in unit tests; no text message or command is sent by the suite. Native transport validation uses Hermes's real contract. See [design](docs/design.md), [plan](docs/plan.md) and [verification](docs/verification.md) for evidence and remaining gates.

MIT licensed. This connector is maintained independently of Nous Research and Photon.
