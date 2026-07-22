# Evidence contract

## Status semantics

### VERIFIED

Use only when every material acceptance claim has current, passing, task-relevant evidence and no material result is unresolved.

### PARTIALLY VERIFIED

Use when performed checks pass but at least one material claim lacks sufficient evidence because of a missing environment, unavailable service, unsupported platform, access restriction, time constraint, or another explicit limitation.

### FAILED

Use when a relevant check fails, observed behavior contradicts a claim, or the final state contains a material defect. A failure remains a failure until explained and rerun successfully on the final revision.

### BLOCKED

Use when no meaningful verification can be performed or a prerequisite prevents reaching a useful conclusion.

## Claim-to-evidence rules

| Claim | Strong evidence | Insufficient by itself |
| --- | --- | --- |
| Bug is fixed | Reproduction fails before and passes after, or a focused regression test passes | Reading the edited code |
| Feature works | Runtime exercise or end-to-end test of the requested path | Successful compilation |
| Types are correct | Project type checker succeeds | Editor diagnostics alone |
| Project builds | Production-shaped build command succeeds | Unit tests alone |
| UI matches request | Rendered UI inspection at relevant viewports | Source markup inspection |
| API remains compatible | Contract tests or consumer-shaped calls | Internal unit tests only |
| Migration is safe | Forward, compatibility, and rollback rehearsal on representative data | Schema file inspection |
| Authorization is correct | Positive and negative identity tests across the boundary | Happy-path request |
| Performance improved | Comparable benchmark with controlled inputs | Subjective impression |
| No regressions | Relevant broader suite plus risk-based checks | One focused test |
| Ready to release | Release artifact build and release-shaped smoke test | Development server run |

## Evidence record

For each material check retain:

- claim or risk addressed;
- exact command or manual procedure;
- final result;
- relevant output summary;
- revision or working-tree state when ambiguity is possible;
- limitation or environmental assumption.

Evidence is current only if it applies to the final state. Re-run a check when later edits can affect its result.

## Unacceptable shortcuts

Do not use these as passing evidence:

- “the code looks correct” for a runtime claim;
- a command from an earlier revision;
- a test file that was added but never executed;
- a swallowed non-zero exit code;
- a screenshot for hidden state or data integrity;
- mocked behavior for a real integration claim;
- an agent's earlier statement that work passed;
- absence of an observed error when the relevant path was not exercised.

## Reporting template

```markdown
Status: VERIFIED | PARTIALLY VERIFIED | FAILED | BLOCKED

| Claim | Evidence | Result |
| --- | --- | --- |
| ... | ... | Pass / Fail / Unavailable |

Unverified:
- None.

Caveats:
- None.
```

Omit empty sections when a one-line statement is clearer. Include only useful excerpts from failing output and remove sensitive values.
