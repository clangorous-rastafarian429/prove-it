# Contributing

Contributions that make verification more honest, portable, or useful are welcome.

## Before opening a pull request

1. Keep the canonical behavior in `skills/prove-it/SKILL.md`.
2. Keep platform adapters concise and semantically aligned with the canonical evidence contract.
3. Avoid adding network services, account requirements, or dependencies without a strong portability reason.
4. Add or update tests for changes to `evidence.py`.
5. Run `make test`.
6. Describe the user-visible behavior and the evidence that supports it in the pull request.

## Design principles

- Never turn an unavailable check into a passing result.
- Never make verification an excuse for unrelated changes.
- Prefer project-native checks over invented commands.
- Preserve command exit codes.
- Minimize collection and retention of command output.
- Keep the core skill readable by multiple agent products.

## Pull requests

Use a focused title, explain the problem, list the final checks performed, and disclose any unverified behavior. Small pull requests are easier to prove.
