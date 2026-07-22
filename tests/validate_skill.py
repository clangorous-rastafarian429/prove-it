from __future__ import annotations

import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "prove-it"
SKILL_FILE = SKILL_ROOT / "SKILL.md"


def fail(message: str) -> None:
    raise ValueError(message)


def main() -> int:
    if not SKILL_FILE.is_file():
        fail("skills/prove-it/SKILL.md is missing")
    content = SKILL_FILE.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    parts = content.split("---\n", 2)
    if len(parts) != 3:
        fail("SKILL.md frontmatter is not closed")
    fields: dict[str, str] = {}
    for line in parts[1].splitlines():
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        if not separator:
            fail(f"Invalid frontmatter line: {line}")
        fields[key.strip()] = value.strip()
    if set(fields) != {"name", "description"}:
        fail("SKILL.md frontmatter must contain only name and description")
    if fields["name"] != "prove-it":
        fail("Skill name must be prove-it")
    if not re.fullmatch(r"[a-z0-9-]{1,63}", fields["name"]):
        fail("Skill name is invalid")
    if len(fields["description"]) < 80:
        fail("Skill description is too short to trigger reliably")
    if "TODO" in content:
        fail("SKILL.md contains an unfinished TODO")
    if len(content.splitlines()) > 500:
        fail("SKILL.md exceeds 500 lines")
    references = re.findall(r"\]\((references/[^)]+)\)", parts[2])
    for reference in references:
        if not (SKILL_ROOT / reference).is_file():
            fail(f"Missing referenced file: {reference}")
    required = [
        SKILL_ROOT / "agents" / "openai.yaml",
        SKILL_ROOT / "scripts" / "evidence.py",
        SKILL_ROOT / "references" / "profiles.md",
        SKILL_ROOT / "references" / "evidence-contract.md",
        SKILL_ROOT / "references" / "ecosystems.md",
    ]
    for path in required:
        if not path.is_file():
            fail(f"Missing required file: {path.relative_to(ROOT)}")
    print("Skill structure is valid")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
