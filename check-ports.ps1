# 🔍 Script de verificación de puertos y conectividad (PowerShell)

Write-Host "🔍 Verificando configuración de puertos..." -ForegroundColor Cyan
Write-Host ""

# Verificar puertos
Write-Host "📡 PUERTOS DEL SISTEMA:" -ForegroundColor Magenta
Write-Host "   FastAPI (API Backend): 8000" -ForegroundColor Gray
Write-Host "   Streamlit (Dashboard): 8501" -ForegroundColor Gray
Write-Host ""

# Verificar si los puertos están en uso
Write-Host "🔍 VERIFICANDO PUERTOS EN USO:" -ForegroundColor Magenta

# Puerto 8000 (API)
$port8000 = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($port8000) {
    Write-Host "   ✅ Puerto 8000: EN USO (API probablemente corriendo)" -ForegroundColor Green
} else {
    Write-Host "   ❌ Puerto 8000: LIBRE (API no está corriendo)" -ForegroundColor Red
}

# Puerto 8501 (Streamlit)
$port8501 = Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue
if ($port8501) {
    Write-Host "   ✅ Puerto 8501: EN USO (Streamlit probablemente corriendo)" -ForegroundColor Green
} else {
    Write-Host "   ❌ Puerto 8501: LIBRE (Streamlit no está corriendo)" -ForegroundColor Red
}

Write-Host ""

# Verificar conectividad del API
Write-Host "🌐 VERIFICANDO CONECTIVIDAD DEL API:" -ForegroundColor Magenta
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "   ✅ API responde en http://localhost:8000/" -ForegroundColor Green
    
    # Verificar endpoint de docs
    try {
        $docsResponse = Invoke-WebRequest -Uri "http://localhost:8000/docs" -TimeoutSec 5 -ErrorAction Stop
        Write-Host "   ✅ Documentación disponible en http://localhost:8000/docs" -ForegroundColor Green
    } catch {
        Write-Host "   ⚠️ Documentación no accesible" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ API no responde en http://localhost:8000/" -ForegroundColor Red
    Write-Host "      💡 Ejecuta: uv run uvicorn api.main:app --host 0.0.0.0 --port 8000" -ForegroundColor Yellow
}

Write-Host ""

# Verificar Dashboard
Write-Host "🎨 VERIFICANDO DASHBOARD:" -ForegroundColor Magenta
try {
    $dashResponse = Invoke-WebRequest -Uri "http://localhost:8501/" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "   ✅ Dashboard responde en http://localhost:8501/" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Dashboard no responde en http://localhost:8501/" -ForegroundColor Red
    Write-Host "      💡 Ejecuta: uv run streamlit run scripts/visualizations/main.py" -ForegroundColor Yellow
}

Write-Host ""

# Verificar variables de entorno
Write-Host "🔧 VARIABLES DE ENTORNO:" -ForegroundColor Magenta
$apiUrl = $env:API_URL
if ($apiUrl) {
    Write-Host "   API_URL = $apiUrl" -ForegroundColor Gray
} else {
    Write-Host "   API_URL = (no configurada, usando default local)" -ForegroundColor Gray
}

$streamlitEnv = $env:STREAMLIT_RUNTIME_ENV
if ($streamlitEnv) {
    Write-Host "   STREAMLIT_RUNTIME_ENV = $streamlitEnv" -ForegroundColor Gray
} else {
    Write-Host "   STREAMLIT_RUNTIME_ENV = (no configurada)" -ForegroundColor Gray
}

Write-Host ""

# Verificar archivos de configuración
Write-Host "📁 ARCHIVOS DE CONFIGURACIÓN:" -ForegroundColor Magenta
if (Test-Path ".streamlit/secrets.toml") {
    Write-Host "   ✅ .streamlit/secrets.toml existe" -ForegroundColor Green
} else {
    Write-Host "   ⚠️ .streamlit/secrets.toml no encontrado" -ForegroundColor Yellow
}

if (Test-Path "pyproject.toml") {
    Write-Host "   ✅ pyproject.toml existe" -ForegroundColor Green
} else {
    Write-Host "   ❌ pyproject.toml no encontrado" -ForegroundColor Red
}

if (Test-Path "Dockerfile") {
    Write-Host "   ✅ Dockerfile existe" -ForegroundColor Green
} else {
    Write-Host "   ❌ Dockerfile no encontrado" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 COMANDOS ÚTILES:" -ForegroundColor Magenta
Write-Host "   Levantar API:       uv run uvicorn api.main:app --host 0.0.0.0 --port 8000" -ForegroundColor Gray
Write-Host "   Levantar Dashboard: uv run streamlit run scripts/visualizations/main.py" -ForegroundColor Gray
Write-Host "   Ver puertos:        Get-NetTCPConnection -LocalPort 8000,8501" -ForegroundColor Gray
Write-Host "   Matar proceso:      Stop-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess" -ForegroundColor Gray
Write-Host ""
Write-Host "📋 Para más detalles: ENVIRONMENT_CONFIG.md" -ForegroundColor Cyan