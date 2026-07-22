# ProveIt

**Make coding agents prove their work before they say “done.”**

ProveIt is a portable Agent Skill for Codex, Claude Code, Cursor, GitHub Copilot, and agents that support the open skills directory convention. It turns completion into an evidence-backed decision using tests, builds, static checks, runtime checks, and honest disclosure of anything that could not be verified.

```text
Before

Done — the login bug is fixed.

After ProveIt

Status: PARTIALLY VERIFIED

✓ Regression test: 6 passed
✓ Type check: passed
✓ Production build: passed
⚠ Real OAuth callback: unavailable without provider credentials
```

## Why ProveIt

Coding agents often confuse a plausible edit with a verified result. ProveIt adds a lightweight completion gate:

- every important claim is mapped to an observable check;
- checks run against the final revision;
- passing, failing, skipped, and unavailable checks remain distinct;
- verification depth scales from quick to strict;
- high-risk changes require negative and boundary evidence;
- the final answer reports proof and gaps instead of confidence theater.

No API key, hosted service, account, or runtime dependency is required. The optional evidence recorder uses only the Python standard library.

## Install

Clone or download this repository, enter its directory, and run:

```bash
./install.sh
```

The installer detects supported agents already present on the machine. If none are detected, it installs the open Agent Skills layout.

Windows PowerShell:

```powershell
./install.ps1
```

Install for a specific agent:

```bash
./install.sh --agent codex
./install.sh --agent claude
./install.sh --agent cursor
./install.sh --agent copilot --scope project
./install.sh --agent generic
```

Install every supported project adapter:

```bash
./install.sh --agent all --scope project
```

The default scope is `user`. Project installation writes only inside the directory supplied with `--project`, which defaults to the current directory.

```bash
./install.sh --agent all --scope project --project /path/to/project
```

Running the installer again updates the installed files.

## Use

Invoke the skill explicitly:

```text
Use $prove-it to verify this change before you call it complete.
```

Other useful prompts:

```text
Use $prove-it in strict mode and tell me whether this authentication fix is ready to merge.
```

```text
Prove that the bug is fixed. Do not change anything else.
```

```text
Verify the final diff and show exactly which claims remain untested.
```

Once installed as an Agent Skill, ProveIt can also trigger automatically for requests involving verification, validation, testing, release readiness, or evidence-backed completion.

## Verification profiles

| Profile | Best for | Minimum depth |
| --- | --- | --- |
| Quick | Small, localized, low-risk edits | Diff inspection, focused check, cheapest static check |
| Standard | Normal features, fixes, and refactors | Focused tests, static checks, broader test/build, primary runtime path |
| Strict | Auth, payments, migrations, security, releases | Standard plus negative, boundary, integration, recovery, and release-shaped checks |

ProveIt defaults to Standard and upgrades automatically when the consequence of being wrong is high.

## Honest statuses

- `VERIFIED`: every material claim has current passing evidence.
- `PARTIALLY VERIFIED`: performed checks pass, but a material check is unavailable.
- `FAILED`: evidence contradicts at least one material claim.
- `BLOCKED`: meaningful verification could not be performed.

A failure never becomes “partial verification” just because other checks passed.

## Evidence recorder

The optional recorder runs a command, preserves its exit status, redacts common secret formats, and appends a JSON Lines evidence record:

```bash
python skills/prove-it/scripts/evidence.py run \
  --label "Unit tests" \
  --log .proveit/evidence.jsonl \
  -- python -m pytest -q
```

Generate a shareable Markdown report:

```bash
python skills/prove-it/scripts/evidence.py render \
  --log .proveit/evidence.jsonl \
  --output .proveit/report.md
```

Fail a pipeline unless every recorded command passed:

```bash
python skills/prove-it/scripts/evidence.py status \
  --log .proveit/evidence.jsonl
```

Add a custom redaction regular expression with `--redact` or the `PROVEIT_REDACT` environment variable. Review reports before publishing them: automatic redaction reduces risk but cannot recognize every secret format.

## Supported layouts

| Target | User installation | Project installation |
| --- | --- | --- |
| Codex | `~/.codex/skills/prove-it` | `.agents/skills/prove-it` |
| Claude Code | `~/.claude/skills/prove-it` | `.claude/skills/prove-it` |
| Generic Agent Skills | `~/.agents/skills/prove-it` | `.agents/skills/prove-it` |
| Cursor | `~/.cursor/rules/prove-it.mdc` | `.cursor/rules/prove-it.mdc` |
| GitHub Copilot | Project scope only | `.github/instructions/prove-it.instructions.md` |

The canonical portable skill lives in [`skills/prove-it`](skills/prove-it). Cursor and Copilot receive compact native adapters derived from the same evidence contract.

## Uninstall

```bash
./uninstall.sh
```

Windows PowerShell:

```powershell
./uninstall.ps1
```

The uninstallers accept the same `--agent`, `--scope`, and project options as the installers and remove only ProveIt-owned paths.

## Safety and privacy

ProveIt does not grant an agent permission to deploy, alter production data, make purchases, install dependencies, contact external services, or expand the requested change. It instructs the agent to stop and disclose a verification gap when meaningful proof would require new authority.

The evidence recorder never captures the full environment. It stores command output tails and basic Git state. Command output can still contain sensitive material, so keep `.proveit/` out of version control unless a reviewed report is intentionally being committed.

## Development

```bash
make test
```

The test suite covers successful and failing commands, exit-code preservation, report generation, output truncation, timeout handling, and secret redaction.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security-sensitive reports should follow [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)
