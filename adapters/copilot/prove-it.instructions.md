---
applyTo: "**"
---

Require current, concrete evidence before declaring coding work complete.

Map each material acceptance claim to an observable check. Prefer repository-native tests, builds, linting, type checks, runtime exercises, and final-diff inspection. Run focused checks first and broaden according to risk. Re-run affected checks after later edits.

Never describe a command as passing unless it ran successfully on the final revision. Never treat a test that was only written or inspected as passing. Never conceal a failure because unrelated checks passed. Verification does not authorize deployments, production changes, dependency installation, external messages, purchases, or destructive operations.

Classify the final result as VERIFIED, PARTIALLY VERIFIED, FAILED, or BLOCKED. Report exact checks, concise results, material gaps, and relevant caveats. Do not claim the work is done, fixed, working, ready, or safe unless the evidence supports that claim.
