param(
    [ValidateSet("Auto", "All", "Codex", "Claude", "Cursor", "Copilot", "Generic")]
    [string]$Agent = "Auto",
    [ValidateSet("User", "Project")]
    [string]$Scope = "User",
    [string]$ProjectPath = (Get-Location).Path
)

$ErrorActionPreference = "Stop"
$ProjectPath = (Resolve-Path $ProjectPath).Path

function Remove-ProveIt([string]$Path) {
    if (Test-Path $Path) {
        Remove-Item -Recurse -Force -Path $Path
        Write-Host "Removed ProveIt: $Path"
    } else {
        Write-Host "Not installed: $Path"
    }
}

$Agents = [System.Collections.Generic.List[string]]::new()

function Add-Agent([string]$Name) {
    if (-not $Agents.Contains($Name)) {
        $Agents.Add($Name)
    }
}

if (($Agent -eq "Auto") -or ($Agent -eq "All")) {
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
        "Generic:User" { Remove-ProveIt (Join-Path $HOME ".agents/skills/prove-it") }
        "Generic:Project" { Remove-ProveIt (Join-Path $ProjectPath ".agents/skills/prove-it") }
        "Codex:User" { Remove-ProveIt (Join-Path $HOME ".codex/skills/prove-it") }
        "Codex:Project" { Remove-ProveIt (Join-Path $ProjectPath ".agents/skills/prove-it") }
        "Claude:User" { Remove-ProveIt (Join-Path $HOME ".claude/skills/prove-it") }
        "Claude:Project" { Remove-ProveIt (Join-Path $ProjectPath ".claude/skills/prove-it") }
        "Cursor:User" { Remove-ProveIt (Join-Path $HOME ".cursor/rules/prove-it.mdc") }
        "Cursor:Project" { Remove-ProveIt (Join-Path $ProjectPath ".cursor/rules/prove-it.mdc") }
        "Copilot:Project" { Remove-ProveIt (Join-Path $ProjectPath ".github/instructions/prove-it.instructions.md") }
        "Copilot:User" { throw "GitHub Copilot installation is supported at project scope." }
    }
}
