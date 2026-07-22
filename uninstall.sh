#!/usr/bin/env bash
set -euo pipefail

AGENT="auto"
SCOPE="user"
PROJECT="$(pwd)"

usage() {
  printf '%s\n' "Usage: ./uninstall.sh [--agent auto|all|codex|claude|cursor|copilot|generic] [--scope user|project] [--project PATH]"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --agent) AGENT="${2:-}"; shift 2 ;;
    --scope) SCOPE="${2:-}"; shift 2 ;;
    --project) PROJECT="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'Unknown argument: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
done

case "$AGENT" in
  auto|all|codex|claude|cursor|copilot|generic) ;;
  *) printf 'Unsupported agent: %s\n' "$AGENT" >&2; exit 2 ;;
esac

case "$SCOPE" in
  user|project) ;;
  *) printf 'Unsupported scope: %s\n' "$SCOPE" >&2; exit 2 ;;
esac

PROJECT="$(cd "$PROJECT" && pwd)"

remove_path() {
  target="$1"
  if [ -e "$target" ]; then
    rm -rf -- "$target"
    printf 'Removed ProveIt: %s\n' "$target"
  else
    printf 'Not installed: %s\n' "$target"
  fi
}

add_agent() {
  candidate="$1"
  case " $AGENTS " in
    *" $candidate "*) ;;
    *) AGENTS="${AGENTS:+$AGENTS }$candidate" ;;
  esac
}

AGENTS=""

if [ "$AGENT" = "auto" ] || [ "$AGENT" = "all" ]; then
  add_agent generic
  [ "$SCOPE" = "user" ] && add_agent codex
  add_agent claude
  add_agent cursor
  [ "$SCOPE" = "project" ] && add_agent copilot
else
  add_agent "$AGENT"
fi

for target_agent in $AGENTS; do
  case "$target_agent:$SCOPE" in
    generic:user) remove_path "$HOME/.agents/skills/prove-it" ;;
    generic:project) remove_path "$PROJECT/.agents/skills/prove-it" ;;
    codex:user) remove_path "$HOME/.codex/skills/prove-it" ;;
    codex:project) remove_path "$PROJECT/.agents/skills/prove-it" ;;
    claude:user) remove_path "$HOME/.claude/skills/prove-it" ;;
    claude:project) remove_path "$PROJECT/.claude/skills/prove-it" ;;
    cursor:user) remove_path "$HOME/.cursor/rules/prove-it.mdc" ;;
    cursor:project) remove_path "$PROJECT/.cursor/rules/prove-it.mdc" ;;
    copilot:project) remove_path "$PROJECT/.github/instructions/prove-it.instructions.md" ;;
    copilot:user) printf '%s\n' 'GitHub Copilot installation is supported at project scope.' >&2; exit 2 ;;
  esac
done
