param(
    [ValidateSet("Auto", "All", "Codex", "Claude", "Cursor", "Copilot", "Generic")]
    [string]$Agent = "Auto",
    [ValidateSet("User", "Project")]
    [string]$Scope = "User",
    [string]$ProjectPath = (Get-Location).Path
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillSource = Join-Path $Root "skills/prove-it"
$ProjectPath = (Resolve-Path $ProjectPath).Path

if (-not (Test-Path (Join-Path $SkillSource "SKILL.md"))) {
    throw "Canonical skill not found: $SkillSource"
}

function Install-Skill([string]$Destination) {
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    Copy-Item -Recurse -Force -Path (Join-Path $SkillSource "*") -Destination $Destination
    Write-Host "Installed ProveIt skill: $Destination"
}

function Install-Adapter([string]$Source, [string]$Destination) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Destination) | Out-Null
    Copy-Item -Force -Path $Source -Destination $Destination
    Write-Host "Installed ProveIt adapter: $Destination"
}

function Has-Command([string]$Name) {
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

$Agents = [System.Collections.Generic.List[string]]::new()

function Add-Agent([string]$Name) {
    if (-not $Agents.Contains($Name)) {
        $Agents.Add($Name)
    }
}

if ($Agent -eq "Auto") {
    if ($Scope -eq "Project") {
        Add-Agent "Generic"
        if (Test-Path (Join-Path $ProjectPath ".claude")) { Add-Agent "Claude" }
        if (Test-Path (Join-Path $ProjectPath ".cursor")) { Add-Agent "Cursor" }
        if (Test-Path (Join-Path $ProjectPath ".github")) { Add-Agent "Copilot" }
    } else {
        if ((Has-Command "codex") -or (Test-Path (Join-Path $HOME ".codex"))) { Add-Agent "Codex" }
        if ((Has-Command "claude") -or (Test-Path (Join-Path $HOME ".claude"))) { Add-Agent "Claude" }
        if ((Has-Command "cursor") -or (Test-Path (Join-Path $HOME ".cursor"))) { Add-Agent "Cursor" }
        if ($Agents.Count -eq 0) { Add-Agent "Generic" }
    }
} elseif ($Agent -eq "All") {
    Add-Agent "Generic"
    if ($Scope -eq "User") { Add-Agent "Codex" }
    Add-Agent "Claude"
    Add-Agent "Cursor"
    if ($Scope -eq "Project") { Add-Agent "Copilot" }
} else {
    Add-Agent $Agent
}

foreach ($TargetAgent in $Agents) {
    $Key = "$TargetAgent`:$Scope"
    switch ($Key) {
        "Generic:User" { Install-Skill (Join-Path $HOME ".agents/skills/prove-it") }
        "Generic:Project" { Install-Skill (Join-Path $ProjectPath ".agents/skills/prove-it") }
        "Codex:User" { Install-Skill (Join-Path $HOME ".codex/skills/prove-it") }
        "Codex:Project" { Install-Skill (Join-Path $ProjectPath ".agents/skills/prove-it") }
        "Claude:User" { Install-Skill (Join-Path $HOME ".claude/skills/prove-it") }
        "Claude:Project" { Install-Skill (Join-Path $ProjectPath ".claude/skills/prove-it") }
        "Cursor:User" { Install-Adapter (Join-Path $Root "adapters/cursor/prove-it.mdc") (Join-Path $HOME ".cursor/rules/prove-it.mdc") }
        "Cursor:Project" { Install-Adapter (Join-Path $Root "adapters/cursor/prove-it.mdc") (Join-Path $ProjectPath ".cursor/rules/prove-it.mdc") }
        "Copilot:Project" { Install-Adapter (Join-Path $Root "adapters/copilot/prove-it.instructions.md") (Join-Path $ProjectPath ".github/instructions/prove-it.instructions.md") }
        "Copilot:User" { throw "GitHub Copilot installation is supported at project scope. Use -Scope Project." }
    }
}

Write-Host 'ProveIt is ready. Ask your agent to use $prove-it before declaring work complete.'
