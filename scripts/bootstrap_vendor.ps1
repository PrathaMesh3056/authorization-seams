# Fetch the pinned upstream checkouts used by the APC pilot.
# The actual work is in scripts/bootstrap_vendor.py so Windows and POSIX shells
# share one implementation.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
python (Join-Path $PSScriptRoot 'bootstrap_vendor.py')
exit $LASTEXITCODE
