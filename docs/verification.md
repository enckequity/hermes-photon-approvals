# Verification

Tested 2026-10-17 on approved DigitalOcean compute, using unchanged official Hermes v0.22.2, revision `d923a5eb487a17c0a68801bba9ef0f56c81040a8`. Development source and temporary databases were isolated from the active gateway. No local runtime was installed, no gateway settings changed and no service restarted.

## Passing evidence

- 26 Python unittest tests: real host transport request binding, approval and denial; native manifest validation, real plugin-manager registration, wrong-home transport invisibility and native dashboard API mounting; verified-session identity/provider/org and expiry; CSRF origin/header/content type; atomic concurrency, duplicate/stale/digest/tenant rejection; private file permissions and symlinks; host interruption and late response; failed card preview updates; secret-safe RPC arguments and failure messages.
- Two Node UI tests: exactly two buttons, no multi-select control, command passed as text, request-bound decision payload, disabled buttons after a decision and no submission from an expired card. These use an SDK/React test harness, not a real browser or iPhone.
- `node --check dashboard/dist/index.js` passed.
- A wheel built successfully in the same DigitalOcean environment using setuptools. Installation still requires the full directory checkout for the native dashboard assets and plugin manifest.
- Fresh independent review found no blocking security issue. Its test-coverage requests were added. Its packaging finding was fixed: the root-only `/dist/` ignore preserves the dashboard assets in the Git release.

## Not established

Photon network calls are mocked in this suite. The earlier separate operator qualification demonstrated Spectrum card send/update and in-Messages opening; it does not prove this plugin's live authenticated approval flow. No live approval card was sent by these tests and no command executed. Native route mounting is tested separately from the real login/device flow.

The private owner runtime currently has no qualified authenticated public dashboard origin or configured approver identity. Activation remains disabled until an operator supplies and qualifies those existing prerequisites. No private dashboard has been exposed. Customer activation also needs the architecture owner's exact runtime/identity handoff and live tenant-denial/lifecycle checks.

Before production, verify login inside Spectrum, the exact configured approver, one harmless command approval and denial, exclusive taps, concurrent requests, expired/replayed/wrong-tenant cards, logout/revocation, restart and device rendering. Keep execution results distinct from a recorded decision. Inline transcript rendering remains device-dependent. Other Hermes releases, dedicated Photon lines and Photon 2 beta projects are unqualified.
