
param([Parameter(Mandatory=$true)][string]$Path,[string]$OutDir = ".\logs\diagnostics")
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$csv = Join-Path $OutDir "events.csv"
$md  = Join-Path $OutDir "events_summary.md"
Get-WinEvent -Path $Path | Select-Object TimeCreated, Id, LevelDisplayName, ProviderName, Message | Export-Csv -NoTypeInformation -Encoding UTF8 $csv
$counts = (Import-Csv $csv | Group-Object ProviderName, LevelDisplayName | Sort-Object Count -Descending)
"# EVTX Summary`n" | Out-File $md -Encoding UTF8
"Source | Level | Count" | Out-File $md -Append
"---|---|---" | Out-File $md -Append
foreach ($c in $counts) { $src,$lvl = $c.Name -split ','; "$src | $lvl | $($c.Count)" | Out-File $md -Append }
Write-Host "Parsed -> $csv , $md"
