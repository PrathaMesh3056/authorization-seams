# Bootstrap commands and failed attempts

Initial working directory: `C:\Users\prath\Downloads\RPaper`.

The following created the new directory and made the first clone attempt. Raw output is in `logs/setup_transcript.txt`.

```powershell
$auditRoot = Join-Path (Get-Location) 'sentinelagent_audit_20261014'
if (Test-Path -LiteralPath $auditRoot) { throw 'Fresh directory already exists' }
New-Item -ItemType Directory -Path $auditRoot | Out-Null
New-Item -ItemType Directory -Path (Join-Path $auditRoot 'logs'),(Join-Path $auditRoot 'audit'),(Join-Path $auditRoot 'runs') | Out-Null
Start-Transcript -Path (Join-Path $auditRoot 'logs/setup_transcript.txt')
git -c core.hooksPath=NUL clone -- https://github.com/ksrpatil/sentinelagent (Join-Path $auditRoot 'upstream')
git -C (Join-Path $auditRoot 'upstream') rev-parse HEAD
git --version
python --version
py -0p
Stop-Transcript
```

It failed with `getaddrinfo() thread failed to start`; the hash command consequently could not find the checkout. Git was `2.52.0.windows.1`; Python was `3.12.7`. `py -0p` printed `No installed Pythons found!`, despite the available `python` executable.

The retry used the audit directory as working directory and setup network access. Raw output is in `logs/clone_retry_transcript.txt`.

```powershell
Start-Transcript -Path 'logs/clone_retry_transcript.txt'
git -c core.hooksPath=NUL clone -- https://github.com/ksrpatil/sentinelagent upstream
$cloneExit = $LASTEXITCODE
if ($cloneExit -eq 0) {
    git -C upstream rev-parse HEAD
    git -C upstream log -1 --format=fuller
    git -C upstream status --porcelain
    rg --files upstream
}
Stop-Transcript
exit $cloneExit
```

The retry succeeded and returned `b7b1add07b7485e99aa3b91882a3f8f879f2e357`. Subsequent measured processes use `audit/launch.py`; their exact argv, environments, timestamps, exit statuses and raw outputs are linked in `COMMANDS.md`.

The first permission review for the optional malformed-input probe timed out before a process was started. The tool explicitly permitted one retry; that retry succeeded. Exact tool error is retained in `logs/permission_review_timeout.txt`. This was not evidence that the probe was unsafe and is not a benchmark outcome.
