
$ErrorActionPreference = 'Stop'
& .\.venv\Scripts\Activate.ps1
Start-Process -WindowStyle Minimized -FilePath python -ArgumentList "host-tools\python\udp_bridge.py"
$cfg = Get-Content .\configs\serial.yml | Out-String
if ($cfg -match 'com_port:\s*(COM\d+)') {
  Start-Process -WindowStyle Minimized -FilePath python -ArgumentList "host-tools\python\serial_to_udp.py"
  Write-Host "Serial->UDP bridge started."
} else {
  Write-Host "Serial bridge disabled; no COM configured."
}
