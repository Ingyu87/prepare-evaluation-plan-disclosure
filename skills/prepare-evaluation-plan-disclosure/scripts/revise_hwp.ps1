param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath,

    [Parameter(Mandatory = $true)]
    [string]$PythonExe
)

$ErrorActionPreference = 'Stop'

$resolvedInput = (Resolve-Path -LiteralPath $InputPath).Path
$resolvedPython = (Resolve-Path -LiteralPath $PythonExe).Path
$resolvedOutput = [System.IO.Path]::GetFullPath($OutputPath)

if ($resolvedInput -eq $resolvedOutput) {
    throw 'Input and output paths must be different.'
}

$outputDirectory = Split-Path -Parent $resolvedOutput
if (-not (Test-Path -LiteralPath $outputDirectory)) {
    New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
}

$temporaryRoot = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
$temporaryDirectory = Join-Path $temporaryRoot ("evaluation-plan-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $temporaryDirectory | Out-Null

$sourceHwpx = Join-Path $temporaryDirectory 'source.hwpx'
$revisedHwpx = Join-Path $temporaryDirectory 'revised.hwpx'
$patcher = Join-Path $PSScriptRoot 'update_hwpx_headers.py'
$hwp = $null

try {
    $hwp = New-Object -ComObject HWPFrame.HwpObject
    $null = $hwp.RegisterModule('FilePathCheckDLL', 'SecurityModule')

    if (-not $hwp.Open($resolvedInput, '', 'forceopen:true')) {
        throw "Could not open input HWP: $resolvedInput"
    }
    if (-not $hwp.SaveAs($sourceHwpx, 'HWPX', '')) {
        throw 'Could not save the intermediate HWPX.'
    }
    $hwp.Clear(1)

    & $resolvedPython $patcher $sourceHwpx $revisedHwpx
    if ($LASTEXITCODE -ne 0) {
        throw 'Could not update the HWPX headers.'
    }

    if (-not $hwp.Open($revisedHwpx, '', 'forceopen:true')) {
        throw 'Could not open the revised HWPX.'
    }
    if (-not $hwp.SaveAs($resolvedOutput, 'HWP', '')) {
        throw 'Could not save the output HWP.'
    }
    $hwp.Clear(1)

    if (-not $hwp.Open($resolvedOutput, '', 'forceopen:true')) {
        throw 'Could not reopen the output HWP for verification.'
    }
    $text = $hwp.GetTextFile('TEXT', '')
    $evaluationMethod = -join ([char[]](0xD3C9, 0xAC00, 0x20, 0xBC29, 0xBC95))
    $andCount = -join ([char[]](0xBC0F, 0x20, 0xD69F, 0xC218))
    $methodPattern = [regex]::Escape($evaluationMethod) + '\s*' + [regex]::Escape($andCount)
    if ($text -notmatch $methodPattern) {
        throw 'Could not verify the evaluation method and count header.'
    }
    $unitHeader = -join ([char[]](0x28, 0xAD50, 0xC218, 0xB7, 0xD559, 0xC2B5, 0x20, 0xB0B4, 0xC6A9, 0x29))
    if (-not $text.Contains($unitHeader)) {
        throw 'Could not verify the teaching and learning content header.'
    }

    Write-Output $resolvedOutput
}
finally {
    if ($null -ne $hwp) {
        try { $hwp.Quit() } catch { }
    }

    $checkedTemporaryDirectory = [System.IO.Path]::GetFullPath($temporaryDirectory)
    if ($checkedTemporaryDirectory.StartsWith($temporaryRoot, [System.StringComparison]::OrdinalIgnoreCase) -and
        (Split-Path -Leaf $checkedTemporaryDirectory).StartsWith('evaluation-plan-')) {
        Remove-Item -LiteralPath $checkedTemporaryDirectory -Recurse -Force -ErrorAction SilentlyContinue
    }
}
