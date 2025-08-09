param(
  [switch]$tests = $false
)
chcp 65001 > $null
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'
$env:CREWAI_TELEMETRY_OPT_OUT='1'; $env:DO_NOT_TRACK='1'; $env:OTEL_SDK_DISABLED='true'

if ($tests) {
  Write-Host "→ running pytest (scoped to ./tests)"
  python -m pip install -q -U pytest
  pytest -q
} else {
  Write-Host "→ running team.py"
  python team.py
}
