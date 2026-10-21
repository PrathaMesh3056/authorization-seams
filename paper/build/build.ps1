# Build the single-column arXiv-style draft with Pandoc + XeLaTeX.
# Run from anywhere; paths are resolved relative to this script.
# Requires: Pandoc 3.12+, a Python 3 interpreter, and XeLaTeX on PATH.
# This script does not modify the manuscript or any frozen artifact.

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
$build = $PSScriptRoot
$paper = Split-Path -Parent $build

function Find-Tool([string]$Name) {
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if (-not $cmd) { throw "$Name not found on PATH. Install it or add it to PATH." }
    return $cmd.Source
}

$pandoc = Find-Tool 'pandoc'
$xelatex = Find-Tool 'xelatex'
$python = if (Get-Command 'python' -ErrorAction SilentlyContinue) { 'python' } else { Find-Tool 'py' }

Push-Location $paper
try {
    & $python (Join-Path $build 'preprocess.py')
    if ($LASTEXITCODE -ne 0) { throw 'preprocess.py failed' }

    & $python (Join-Path $build 'retable.py')
    if ($LASTEXITCODE -ne 0) { throw 'retable.py failed' }

    $source = Join-Path $build 'manuscript_build_wide.md'
    $tex = Join-Path $build 'manuscript_build_wide.tex'
    $header = Join-Path $build 'header.tex'
    & $pandoc $source -f markdown -t latex -s `
        --shift-heading-level-by=-1 `
        "--include-in-header=$header" `
        -V geometry:margin=0.75in -V geometry:letterpaper -V fontsize=10pt `
        -o $tex
    if ($LASTEXITCODE -ne 0) { throw 'pandoc failed' }

    & $python (Join-Path $build 'fix_texttt.py')
    if ($LASTEXITCODE -ne 0) { throw 'fix_texttt.py failed' }

    $savedEap = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    $console = Join-Path $build 'xelatex_console.log'
    # Start from a clean label state so convergence does not depend on a stale
    # aux file from an earlier manuscript revision.
    Remove-Item -LiteralPath (Join-Path $build 'manuscript_build_wide.aux') -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath (Join-Path $build 'manuscript_build_wide.out') -ErrorAction SilentlyContinue
    for ($pass = 1; $pass -le 3; $pass++) {
        $cmdLine = '"' + $xelatex + '" -interaction=nonstopmode -halt-on-error ' +
            '"-output-directory=' + $build + '" "' + $tex + '" > "' + $console + '" 2>&1'
        & cmd.exe /d /c $cmdLine
        $code = $LASTEXITCODE
        if ($code -ne 0) {
            $ErrorActionPreference = $savedEap
            throw "xelatex pass $pass failed with exit $code; see $console"
        }
    }
    $ErrorActionPreference = $savedEap

    $log = Join-Path $build 'manuscript_build_wide.log'
    $pdf = Join-Path $build 'manuscript_build_wide.pdf'
    if (-not (Test-Path -LiteralPath $pdf)) { throw "PDF not produced: $pdf" }

    $missing = (Select-String -LiteralPath $log -Pattern 'Missing character' | Measure-Object).Count
    $overfull = (Select-String -LiteralPath $log -Pattern 'Overfull \\hbox' | Measure-Object).Count
    $errors = (Select-String -LiteralPath $log -Pattern '^!|LaTeX Error|Fatal error' | Measure-Object).Count
    $underfull = (Select-String -LiteralPath $log -Pattern 'Underfull \\hbox' | Measure-Object).Count
    $labels = (Select-String -LiteralPath $log -Pattern 'Label\(s\) may have changed' | Measure-Object).Count
    Write-Host "PDF: $pdf"
    Write-Host "Missing glyphs: $missing"
    Write-Host "Overfull hboxes: $overfull"
    Write-Host "Underfull hboxes: $underfull"
    Write-Host "LaTeX errors: $errors"
    Write-Host "Label-changed warnings: $labels"
}
finally {
    Pop-Location
}
