# Open a folder picker and import into library/{program}/{unit}/en/
# Usage: .\scripts\ingest_unit.browse.ps1 -Program tfs -Unit u01
param(
    [Parameter(Mandatory = $true)]
    [string]$Program,
    [Parameter(Mandatory = $true)]
    [string]$Unit
)

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
py -3 scripts/ingest_unit.py --program $Program --unit $Unit --browse
exit $LASTEXITCODE
