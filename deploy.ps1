# 🚀 Script de deployment rápido para Seminario Grupo 5
# Ejecutar desde PowerShell en la raíz del proyecto

Write-Host "🚀 Iniciando deployment desde rama feature/visualizations-ss..." -ForegroundColor Green

# Verificar que estamos en la rama correcta
$currentBranch = git branch --show-current
if ($currentBranch -ne "feature/visualizations-ss") {
    Write-Host "⚠️ No estás en la rama feature/visualizations-ss" -ForegroundColor Yellow
    Write-Host "Rama actual: $currentBranch" -ForegroundColor Yellow
    Write-Host "Cambiando a feature/visualizations-ss..." -ForegroundColor Yellow
    git checkout feature/visualizations-ss
}

Write-Host "✅ En la rama correcta: feature/visualizations-ss" -ForegroundColor Green

# Verificar uv
Write-Host "🔍 Verificando uv..." -ForegroundColor Cyan
try {
    $uvVersion = uv --version
    Write-Host "✅ $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ uv no está instalado. Instalando..." -ForegroundColor Red
    pip install uv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error instalando uv" -ForegroundColor Red
        exit 1
    }
}

# Instalar dependencias
Write-Host "📦 Instalando dependencias..." -ForegroundColor Cyan
uv sync
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error instalando dependencias" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dependencias instaladas" -ForegroundColor Green

# Ejecutar pipeline
Write-Host "🔄 Ejecutando pipeline ETL..." -ForegroundColor Cyan
uv run scripts/pipeline/main.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error ejecutando pipeline" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Pipeline completado" -ForegroundColor Green

# Verificar archivos de salida
$csvPath = "output/cleaned_data/Final Dataframe.csv"
if (Test-Path $csvPath) {
    Write-Host "✅ Archivo CSV generado correctamente" -ForegroundColor Green
    $fileInfo = Get-Item $csvPath
    $fileSize = [math]::Round($fileInfo.Length / 1MB, 2)
    Write-Host "   Tamaño: $fileSize MB" -ForegroundColor Gray
} else {
    Write-Host "❌ No se generó el archivo CSV" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎯 OPCIONES DE DEPLOYMENT:" -ForegroundColor Magenta
Write-Host ""
Write-Host "1️⃣ LOCAL - Docker:" -ForegroundColor White
Write-Host "   docker build -t seminario-grupo5 ." -ForegroundColor Gray
Write-Host "   docker run -p 8000:8000 seminario-grupo5" -ForegroundColor Gray
Write-Host ""
Write-Host "2️⃣ LOCAL - Streamlit:" -ForegroundColor White
Write-Host "   uv run streamlit run scripts/visualizations/main.py" -ForegroundColor Gray
Write-Host ""
Write-Host "3️⃣ CLOUD - Railway:" -ForegroundColor White
Write-Host "   1. Fork repo en GitHub" -ForegroundColor Gray
Write-Host "   2. Conectar a https://railway.app" -ForegroundColor Gray
Write-Host "   3. Seleccionar rama: feature/visualizations-ss" -ForegroundColor Gray
Write-Host "   4. Deploy automático" -ForegroundColor Gray
Write-Host ""
Write-Host "4️⃣ CLOUD - Render:" -ForegroundColor White
Write-Host "   1. Fork repo en GitHub" -ForegroundColor Gray
Write-Host "   2. Conectar a https://render.com" -ForegroundColor Gray
Write-Host "   3. Usar render.yaml configurado" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ Proyecto listo para deployment!" -ForegroundColor Green
Write-Host "📋 Ver DEPLOYMENT_GUIDE.md para detalles completos" -ForegroundColor Cyan