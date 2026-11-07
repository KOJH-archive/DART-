param(
    [switch]$CheckOnly,
    [ValidateRange(1024, 65535)][int]$Port = 8501,
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

$projectDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $projectDirectory ".venv\Scripts\python.exe"
$requirementsFile = Join-Path $projectDirectory "requirements.txt"
$envFile = Join-Path $projectDirectory ".env"
$envExample = Join-Path $projectDirectory ".env.example"
$appUrl = "http://127.0.0.1:$Port"
$ollamaUrl = "http://127.0.0.1:11434"

Set-Location -LiteralPath $projectDirectory

function Write-Step([string]$Message) {
    Write-Host "`n[DART] $Message" -ForegroundColor Cyan
}

function Read-EnvValue([string]$Name, [string]$DefaultValue) {
    if (Test-Path -LiteralPath $envFile) {
        foreach ($line in Get-Content -LiteralPath $envFile -Encoding UTF8) {
            if ($line -match ('^' + [regex]::Escape($Name) + '=(.*)$')) {
                $value = $matches[1].Trim()
                if ($value) {
                    return $value
                }
            }
        }
    }
    return $DefaultValue
}

$pythonLauncher = Get-Command py.exe -ErrorAction SilentlyContinue
if (-not $pythonLauncher) {
    $pythonLauncher = Get-Command python.exe -ErrorAction SilentlyContinue
}
if (-not $pythonLauncher) {
    throw "Python 3.11 이상을 찾지 못했습니다. Python을 설치한 뒤 다시 실행해 주세요."
}

$ollamaCommand = Get-Command ollama.exe -ErrorAction SilentlyContinue
if (-not $ollamaCommand) {
    throw "Ollama를 찾지 못했습니다. Ollama를 설치한 뒤 다시 실행해 주세요."
}

if ($CheckOnly) {
    Write-Host "런처 문법과 필수 프로그램 경로를 확인했습니다." -ForegroundColor Green
    Write-Host "Python: $($pythonLauncher.Source)"
    Write-Host "Ollama: $($ollamaCommand.Source)"
    Write-Host "가상환경: $(if (Test-Path -LiteralPath $venvPython) { '준비됨' } else { '첫 실행 시 생성' })"
    exit 0
}

if (-not (Test-Path -LiteralPath $envFile)) {
    Copy-Item -LiteralPath $envExample -Destination $envFile
    Write-Host ".env 파일을 만들었습니다. 실제 기업 조회 전 DART_API_KEY를 입력해 주세요." -ForegroundColor Yellow
}

if (-not (Test-Path -LiteralPath $venvPython)) {
    Write-Step "Python 가상환경을 만드는 중입니다."
    if ($pythonLauncher.Name -eq "py.exe") {
        & $pythonLauncher.Source -3 -m venv ".venv"
    } else {
        & $pythonLauncher.Source -m venv ".venv"
    }
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $venvPython)) {
        throw "Python 가상환경을 만들지 못했습니다."
    }
}

$previousErrorAction = $ErrorActionPreference
$ErrorActionPreference = "SilentlyContinue"
$dependencyProbe = @'
import streamlit, pandas, plotly, httpx, openpyxl, lxml, defusedxml, dotenv
import sys
from pathlib import Path
from importlib.metadata import version
from packaging.requirements import Requirement
assert sys.version_info >= (3, 11), 'Python 3.11 or newer is required'
for line in Path('requirements.txt').read_text(encoding='utf-8').splitlines():
    if line.strip() and not line.lstrip().startswith('#'):
        requirement = Requirement(line)
        assert version(requirement.name) in requirement.specifier, requirement.name
'@
& $venvPython -c $dependencyProbe 2>$null
$dependencyCheckExit = $LASTEXITCODE
$ErrorActionPreference = $previousErrorAction
if ($dependencyCheckExit -ne 0) {
    Write-Step "필요한 Python 패키지를 설치하는 중입니다. 첫 실행에는 몇 분이 걸릴 수 있습니다."
    & $venvPython -m pip install -r $requirementsFile
    if ($LASTEXITCODE -ne 0) {
        throw "Python 패키지 설치에 실패했습니다. 인터넷 연결을 확인해 주세요."
    }
}

Write-Step "로컬 Ollama 서비스를 확인하는 중입니다."
$ollamaReady = $false
try {
    $null = Invoke-RestMethod -Uri "$ollamaUrl/api/tags" -Method Get -TimeoutSec 2
    $ollamaReady = $true
} catch {
    Start-Process -FilePath $ollamaCommand.Source -ArgumentList "serve" -WindowStyle Hidden
    for ($attempt = 0; $attempt -lt 40; $attempt++) {
        Start-Sleep -Milliseconds 500
        try {
            $null = Invoke-RestMethod -Uri "$ollamaUrl/api/tags" -Method Get -TimeoutSec 2
            $ollamaReady = $true
            break
        } catch {
        }
    }
}
if (-not $ollamaReady) {
    throw "Ollama 로컬 서비스가 시작되지 않았습니다. Ollama 앱을 실행한 뒤 다시 시도해 주세요."
}

$ollamaModel = Read-EnvValue "OLLAMA_MODEL" "qwen3.5:4b"
$availableModels = Invoke-RestMethod -Uri "$ollamaUrl/api/tags" -Method Get -TimeoutSec 5
$modelNames = @($availableModels.models | ForEach-Object { $_.name })
if ($ollamaModel -notin $modelNames) {
    throw "Ollama 모델 '$ollamaModel'이 없습니다. 터미널에서 'ollama pull $ollamaModel'을 실행해 주세요."
}

Write-Step "DART 기업분석실을 시작합니다. 종료하려면 이 창에서 Ctrl+C를 누르세요."
$browserJob = $null
if (-not $NoBrowser) {
$browserJob = Start-Job -ScriptBlock {
    param($HealthUrl, $BrowserUrl)
    for ($attempt = 0; $attempt -lt 60; $attempt++) {
        Start-Sleep -Milliseconds 500
        try {
            $null = Invoke-WebRequest -UseBasicParsing -Uri $HealthUrl -TimeoutSec 2
            Start-Process $BrowserUrl
            return
        } catch {
        }
    }
} -ArgumentList "$appUrl/_stcore/health", $appUrl
}

try {
    & $venvPython -m streamlit run "app.py" --server.address "127.0.0.1" --server.port $Port
    if ($LASTEXITCODE -ne 0) {
        throw "Streamlit이 종료 코드 $LASTEXITCODE 로 중단됐습니다."
    }
} finally {
    if ($browserJob) {
        Stop-Job -Job $browserJob -ErrorAction SilentlyContinue
        Remove-Job -Job $browserJob -Force -ErrorAction SilentlyContinue
    }
}
