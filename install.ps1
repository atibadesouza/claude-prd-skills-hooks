# Install Claude PRD/skills/hooks template into a target project's .claude/ dir (Windows / PowerShell).
# Usage:
#   .\install.ps1                # installs into the current directory
#   .\install.ps1 C:\path\to\repo  # installs into the given repo

param(
    [string]$Target = (Get-Location).Path
)

$Src = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Test-Path $Target -PathType Container)) {
    Write-Error "Target directory does not exist: $Target"
    exit 1
}

$null = New-Item -ItemType Directory -Force -Path "$Target\.claude\hooks"
$null = New-Item -ItemType Directory -Force -Path "$Target\.claude\skills"
$null = New-Item -ItemType Directory -Force -Path "$Target\docs\plans"

Copy-Item "$Src\.claude\hooks\post-commit-pitfalls.mjs" "$Target\.claude\hooks\" -Force
Copy-Item "$Src\.claude\hooks\save-plan.mjs"            "$Target\.claude\hooks\" -Force
Copy-Item "$Src\.claude\skills\quickpush"               "$Target\.claude\skills\" -Recurse -Force

$Settings = "$Target\.claude\settings.json"
if (Test-Path $Settings) {
    Write-Host "NOTE: $Settings already exists - not overwriting."
    Write-Host "      Merge the PostToolUse entries from $Src\.claude\settings.json manually."
} else {
    Copy-Item "$Src\.claude\settings.json" $Settings -Force
}

Write-Host "Installed Claude hooks + quickpush skill into $Target\.claude\"
Write-Host "Hooks installed:"
Write-Host "  - post-commit-pitfalls.mjs  (PostToolUse / Bash -> updates PITFALLS.md)"
Write-Host "  - save-plan.mjs             (PostToolUse / ExitPlanMode -> docs\plans\*.md)"
Write-Host "Skill installed: quickpush"
