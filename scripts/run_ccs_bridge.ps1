
$ErrorActionPreference = 'Stop'
& .\.venv\Scripts\Activate.ps1
$cfg = (Get-Content .\configs\ccs.yml | Out-String)
if ($cfg -match 'mode:\s*(\w+)') { $mode = $Matches[1] } else { $mode = 'tcp' }

switch ($mode) {
  'tcp'   { python host-tools\python\ccs_socket_bridge.py }
  'file'  { python host-tools\python\ccs_file_streamer.py }
  'rest'  { python host-tools\python\ccs_http_push.py }
  'serial'{ python host-tools\python\ccs_com_emulator.py }
  default { Write-Error "Unknown mode: $mode" }
}
