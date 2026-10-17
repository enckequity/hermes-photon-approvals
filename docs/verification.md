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

## Live-button probe and corrective release

On 2026-10-17, an operator received a harmless static demo sent through Spectrum with `live: true` and explicitly confirmed both that Approve/Deny buttons were visible in the message bubble and that they worked without opening a panel. The demo changes local display only, resets on reload, and has no command authority, storage or server callback. This qualifies inline rendering on that tested device, not the authenticated approval flow. Demo source is in `demo/` (PR #5).

The probe exposed two v0.1.0 defects hidden by mocked network tests: `MiniAppLayout.summaryText` was not a valid proto field, and the default urllib user agent received Cloudflare HTTP403. v0.1.1 uses the actual `summary` field and a descriptive connector user agent; a live token-only check with that user agent returned HTTP200 and a shared-line token. All 28 Python tests and four Node tests (including the demo) passed on DigitalOcean for this fix. A regression test now parses both send and update payloads against descriptors generated from the installed official 2.3.0 proto schemas. It reproduced the invalid-field failure before the fix. No automatic resend followed an uncertain delivery; the invalid field was confirmed as a local pre-transmission parsing failure before the corrected send.
