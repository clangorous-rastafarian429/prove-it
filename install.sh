#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SOURCE="$ROOT/skills/prove-it"
AGENT="auto"
SCOPE="user"
PROJECT="$(pwd)"

usage() {
  printf '%s\n' "Usage: ./install.sh [--agent auto|all|codex|claude|cursor|copilot|generic] [--scope user|project] [--project PATH]"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --agent)
      AGENT="${2:-}"
      shift 2
      ;;
    --scope)
      SCOPE="${2:-}"
      shift 2
      ;;
    --project)
      PROJECT="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
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

if [ ! -f "$SKILL_SOURCE/SKILL.md" ]; then
  printf 'Canonical skill not found: %s\n' "$SKILL_SOURCE" >&2
  exit 1
fi

PROJECT="$(cd "$PROJECT" && pwd)"

install_skill() {
  destination="$1"
  mkdir -p "$destination"
  cp -R "$SKILL_SOURCE/." "$destination/"
  printf 'Installed ProveIt skill: %s\n' "$destination"
}

install_file() {
  source_file="$1"
  destination="$2"
  mkdir -p "$(dirname "$destination")"
  cp "$source_file" "$destination"
  printf 'Installed ProveIt adapter: %s\n' "$destination"
}

add_agent() {
  candidate="$1"
  case " $AGENTS " in
    *" $candidate "*) ;;
    *) AGENTS="${AGENTS:+$AGENTS }$candidate" ;;
  esac
}

AGENTS=""

if [ "$AGENT" = "auto" ]; then
  if [ "$SCOPE" = "project" ]; then
    add_agent generic
    [ -d "$PROJECT/.claude" ] && add_agent claude
    [ -d "$PROJECT/.cursor" ] && add_agent cursor
    [ -d "$PROJECT/.github" ] && add_agent copilot
  else
    command -v codex >/dev/null 2>&1 || [ -d "$HOME/.codex" ] && add_agent codex
    command -v claude >/dev/null 2>&1 || [ -d "$HOME/.claude" ] && add_agent claude
    command -v cursor >/dev/null 2>&1 || [ -d "$HOME/.cursor" ] && add_agent cursor
    [ -n "$AGENTS" ] || add_agent generic
  fi
elif [ "$AGENT" = "all" ]; then
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
    generic:user) install_skill "$HOME/.agents/skills/prove-it" ;;
    generic:project) install_skill "$PROJECT/.agents/skills/prove-it" ;;
    codex:user) install_skill "$HOME/.codex/skills/prove-it" ;;
    codex:project) install_skill "$PROJECT/.agents/skills/prove-it" ;;
    claude:user) install_skill "$HOME/.claude/skills/prove-it" ;;
    claude:project) install_skill "$PROJECT/.claude/skills/prove-it" ;;
    cursor:user) install_file "$ROOT/adapters/cursor/prove-it.mdc" "$HOME/.cursor/rules/prove-it.mdc" ;;
    cursor:project) install_file "$ROOT/adapters/cursor/prove-it.mdc" "$PROJECT/.cursor/rules/prove-it.mdc" ;;
    copilot:project) install_file "$ROOT/adapters/copilot/prove-it.instructions.md" "$PROJECT/.github/instructions/prove-it.instructions.md" ;;
    copilot:user) printf '%s\n' 'GitHub Copilot installation is supported at project scope. Use --scope project.' >&2; exit 2 ;;
  esac
done

printf '%s\n' 'ProveIt is ready. Ask your agent to use $prove-it before declaring work complete.'
