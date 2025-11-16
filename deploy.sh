#!/bin/bash
# 🚀 Script de deployment rápido para Seminario Grupo 5
# Ejecutar desde la raíz del proyecto

echo "🚀 Iniciando deployment desde rama feature/visualizations-ss..."

# Verificar que estamos en la rama correcta
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "feature/visualizations-ss" ]; then
    echo "⚠️ No estás en la rama feature/visualizations-ss"
    echo "Rama actual: $CURRENT_BRANCH"
    echo "Cambiando a feature/visualizations-ss..."
    git checkout feature/visualizations-ss
fi

echo "✅ En la rama correcta: feature/visualizations-ss"

# Verificar uv
echo "🔍 Verificando uv..."
if ! command -v uv &> /dev/null; then
    echo "❌ uv no está instalado. Instalando..."
    pip install uv
fi
echo "✅ uv $(uv --version)"

# Instalar dependencias
echo "📦 Instalando dependencias..."
uv sync
if [ $? -ne 0 ]; then
    echo "❌ Error instalando dependencias"
    exit 1
fi
echo "✅ Dependencias instaladas"

# Ejecutar pipeline
echo "🔄 Ejecutando pipeline ETL..."
uv run scripts/pipeline/main.py
if [ $? -ne 0 ]; then
    echo "❌ Error ejecutando pipeline"
    exit 1
fi
echo "✅ Pipeline completado"

# Verificar archivos de salida
if [ -f "output/cleaned_data/Final Dataframe.csv" ]; then
    echo "✅ Archivo CSV generado correctamente"
    FILE_SIZE=$(ls -lh "output/cleaned_data/Final Dataframe.csv" | awk '{print $5}')
    echo "   Tamaño: $FILE_SIZE"
else
    echo "❌ No se generó el archivo CSV"
    exit 1
fi

echo ""
echo "🎯 OPCIONES DE DEPLOYMENT:"
echo ""
echo "1️⃣ LOCAL - Docker:"
echo "   docker build -t seminario-grupo5 ."
echo "   docker run -p 8000:8000 seminario-grupo5"
echo ""
echo "2️⃣ LOCAL - Streamlit:"
echo "   uv run streamlit run scripts/visualizations/main.py"
echo ""
echo "3️⃣ CLOUD - Railway:"
echo "   1. Fork repo en GitHub"
echo "   2. Conectar a https://railway.app"
echo "   3. Seleccionar rama: feature/visualizations-ss"
echo "   4. Deploy automático"
echo ""
echo "4️⃣ CLOUD - Render:"
echo "   1. Fork repo en GitHub"
echo "   2. Conectar a https://render.com"
echo "   3. Usar render.yaml configurado"
echo ""
echo "✅ Proyecto listo para deployment!"
echo "📋 Ver DEPLOYMENT_GUIDE.md para detalles completos"