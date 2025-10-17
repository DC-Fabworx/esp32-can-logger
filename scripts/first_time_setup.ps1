
param([switch]$SkipFirewall)
$ErrorActionPreference = 'Stop'
Write-Host "== First-time setup =="

if (-not (Test-Path ".\.venv")) { & py -3 -m venv .venv }
& .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r .\host-tools\python\requirements.txt

if (-not $SkipFirewall) { & .\host-tools\windows\open_firewall_ports.bat | Out-Host }

$ports = Get-PnpDevice -Class 'Ports' -Status OK | Select FriendlyName, InstanceId
$comPort = $null
foreach ($p in $ports) { if ($p.FriendlyName -match '(COM\d+)') { $comPort = $Matches[1]; break } }
if ($comPort) {
  (Get-Content .\configs\serial.yml) -replace 'com_port:.*',("com_port: {0}" -f $comPort) | Set-Content .\configs\serial.yml
  Write-Host "Detected COM: $comPort"
} else {
  Write-Warning "No COM detected. Serial bridge will be disabled."
}
