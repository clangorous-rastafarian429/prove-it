---
name: prove-it
description: Require concrete, task-relevant evidence before declaring coding work complete. Use when implementing, fixing, refactoring, migrating, reviewing, or preparing software for release; when a user asks to verify, validate, test, prove, double-check, or show that a change works; or when completion claims should be backed by tests, builds, static checks, runtime checks, screenshots, or other observable results. Apply to code and configuration changes across ecosystems, including agent-authored work. Do not use evidence from an earlier revision as proof of the current revision.
---

# ProveIt

Treat completion as a claim that needs current evidence. Match verification effort to risk, execute the strongest safe checks available, and report both proof and gaps without implying more certainty than the evidence supports.

## Core rules

1. Verify the final state, not an intermediate revision.
2. Map every important acceptance claim to at least one observable check.
3. Prefer behavior-level evidence over inspection, and inspection over intuition.
4. Never describe a command as passing unless it ran successfully in this task.
5. Never treat a test that was merely written, discovered, or read as a passing test.
6. Preserve the user's scope. Verification does not authorize unrelated fixes, deployments, external writes, or destructive actions.
7. Surface skipped, unavailable, flaky, or inconclusive checks explicitly.
8. Re-run affected checks after any verification-driven edit.
9. Keep credentials, tokens, personal data, and proprietary output out of reports.
10. Use `VERIFIED` only when all material claims are supported and no material check remains unresolved.

## Workflow

### 1. Define the claims

Translate the request and implemented changes into a short claim set. Include user-visible behavior, regression-sensitive behavior, and important non-functional constraints. Use repository instructions and stated acceptance criteria as authoritative.

For each claim, record:

- what must be true;
- the best available verification method;
- the expected observable result;
- the risk if the claim is wrong.

Do not inflate the claim set with unrelated quality goals.

### 2. Select a profile

Choose `quick`, `standard`, or `strict` using [references/profiles.md](references/profiles.md). Honor an explicit user-selected profile. Default to `standard`; upgrade when the change affects authentication, authorization, payments, secrets, migrations, destructive operations, concurrency, public APIs, releases, or production configuration.

### 3. Discover project-native checks

Read relevant repository instructions and inspect manifests, task runners, CI workflows, and nearby tests. Prefer the project's documented commands. Consult [references/ecosystems.md](references/ecosystems.md) only when commands are unclear.

Before running a command, check that it is:

- relevant to a claim;
- safe within the user's scope;
- unlikely to mutate external systems or production data;
- appropriately bounded for the selected profile.

Do not install dependencies, update lockfiles, contact paid services, deploy, or run destructive tests unless the task already authorizes it.

### 4. Inspect the final change

Review the final diff and working-tree state. Check for unintended files, debug output, generated artifacts, missing call sites, stale references, merge markers, formatting damage, and accidental secret material.

Inspection can prove structural claims. It cannot by itself prove runtime behavior.

### 5. Execute evidence in layers

Run the smallest high-signal checks first, then broaden as the profile requires:

1. focused regression or unit test;
2. relevant lint, formatting, type, schema, or compile check;
3. broader test or build command;
4. runtime, integration, browser, CLI, or visual check;
5. risk-specific negative, boundary, security, migration, or rollback check.

Stop and report if continuing would be unsafe, materially expensive, or outside authorization. A failed check is evidence, not an inconvenience to hide.

### 6. Record evidence

Capture the exact command or procedure, result, and relevant output. Use the bundled recorder when a durable local report is useful and writing project-local artifacts is authorized:

```bash
python /absolute/path/to/prove-it/scripts/evidence.py run \
  --label "Focused tests" \
  --log .proveit/evidence.jsonl \
  -- pytest tests/test_feature.py -q
```

Render a Markdown report with:

```bash
python /absolute/path/to/prove-it/scripts/evidence.py render \
  --log .proveit/evidence.jsonl \
  --output .proveit/report.md
```

The recorder uses only the Python standard library, truncates stored output, applies common secret redaction patterns, and preserves the wrapped command's exit status. Do not use it when the project must remain untouched; report evidence directly instead.

### 7. Apply the completion gate

Classify the outcome using [references/evidence-contract.md](references/evidence-contract.md):

- `VERIFIED`: every material claim has current passing evidence;
- `PARTIALLY VERIFIED`: available checks pass, but a material check could not be performed;
- `FAILED`: at least one material claim has contradictory or failing evidence;
- `BLOCKED`: meaningful verification could not be performed.

Do not downgrade a real failure to `PARTIALLY VERIFIED`. Do not call work ready to merge or ship when the status is `FAILED` or `BLOCKED`.

### 8. Report concisely

Lead with the status and the conclusion. Then provide a compact evidence table:

| Claim | Check | Result |
| --- | --- | --- |
| Requested behavior | Exact command or procedure | Pass, fail, or unavailable |

Include:

- status;
- material checks that passed;
- failures with the useful error detail;
- unverified claims and why they remain unverified;
- any caveat needed to interpret the result.

Avoid raw log dumps unless the user requests them. Never include secrets or sensitive data.

## Evidence quality

Prefer evidence in this order when applicable:

1. observed end-to-end behavior;
2. focused automated regression test;
3. integration or contract test;
4. successful build, compile, type, schema, or static check;
5. direct inspection of the final diff and state;
6. reasoned inference.

Use lower-ranked evidence when higher-ranked checks are unavailable, but reflect the limitation in the status. Screenshots prove visible state only; they do not prove hidden behavior. Mocks prove the mocked contract only; they do not prove a real integration.

## Failure handling

When a check fails:

1. determine whether the failure is caused by the change, the environment, or a pre-existing issue;
2. preserve the failure evidence;
3. fix only when implementation or repair is within the user's request;
4. rerun the failed check and any newly affected checks;
5. report persistent or pre-existing failures without concealing them.

When a check is flaky, run it enough to characterize the instability if doing so is inexpensive and safe. Do not report a single later pass as conclusive proof after an unexplained failure.

## Resources

- Read [references/profiles.md](references/profiles.md) to choose verification depth.
- Read [references/evidence-contract.md](references/evidence-contract.md) for status semantics and acceptable proof.
- Read [references/ecosystems.md](references/ecosystems.md) when discovering commands in an unfamiliar project.
- Run [scripts/evidence.py](scripts/evidence.py) to capture commands and render a redacted evidence report.
