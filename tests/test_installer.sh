#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMP_PARENT="${TMPDIR:-${RUNNER_TEMP:-$ROOT}}"
mkdir -p "$TEMP_PARENT"
TEST_ROOT="$(mktemp -d "$TEMP_PARENT/proveit-installer.XXXXXX")"
TEST_HOME="$TEST_ROOT/home"
TEST_PROJECT="$TEST_ROOT/project"

cleanup() {
  rm -rf -- "$TEST_ROOT"
}

trap cleanup EXIT

mkdir -p "$TEST_HOME" "$TEST_PROJECT/.github" "$TEST_PROJECT/.claude" "$TEST_PROJECT/.cursor"

HOME="$TEST_HOME" "$ROOT/install.sh" --agent all --scope user
HOME="$TEST_HOME" "$ROOT/install.sh" --agent all --scope project --project "$TEST_PROJECT"

test -f "$TEST_HOME/.agents/skills/prove-it/SKILL.md"
test -f "$TEST_HOME/.codex/skills/prove-it/SKILL.md"
test -f "$TEST_HOME/.claude/skills/prove-it/SKILL.md"
test -f "$TEST_HOME/.cursor/rules/prove-it.mdc"
test -f "$TEST_PROJECT/.agents/skills/prove-it/SKILL.md"
test -f "$TEST_PROJECT/.claude/skills/prove-it/SKILL.md"
test -f "$TEST_PROJECT/.cursor/rules/prove-it.mdc"
test -f "$TEST_PROJECT/.github/instructions/prove-it.instructions.md"

HOME="$TEST_HOME" "$ROOT/uninstall.sh" --agent all --scope user
HOME="$TEST_HOME" "$ROOT/uninstall.sh" --agent all --scope project --project "$TEST_PROJECT"

test ! -e "$TEST_HOME/.agents/skills/prove-it"
test ! -e "$TEST_HOME/.codex/skills/prove-it"
test ! -e "$TEST_HOME/.claude/skills/prove-it"
test ! -e "$TEST_HOME/.cursor/rules/prove-it.mdc"
test ! -e "$TEST_PROJECT/.agents/skills/prove-it"
test ! -e "$TEST_PROJECT/.claude/skills/prove-it"
test ! -e "$TEST_PROJECT/.cursor/rules/prove-it.mdc"
test ! -e "$TEST_PROJECT/.github/instructions/prove-it.instructions.md"

printf '%s\n' "Installer round-trip passed"
