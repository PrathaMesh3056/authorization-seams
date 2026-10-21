param([Parameter(Mandatory=$true)][string]$Name,
      [Parameter(Mandatory=$true)][string]$Executable,
      [string[]]$Arguments = @())
$ErrorActionPreference = 'Stop'
$artifactRoot = $PSScriptRoot
Set-Location -LiteralPath $artifactRoot
$record = @{ executable=$Executable; arguments=$Arguments; cwd=$artifactRoot }
$record | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath "logs/$Name.command.json"
$ErrorActionPreference = 'Continue'
& $Executable @Arguments 2>&1 | Tee-Object -FilePath "logs/$Name.output.txt"
$code = $LASTEXITCODE
$code | Set-Content -LiteralPath "logs/$Name.exitcode.txt"
exit $code
