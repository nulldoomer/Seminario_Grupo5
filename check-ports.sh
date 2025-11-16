#!/bin/bash
# 🔍 Script de verificación de puertos y conectividad

echo "🔍 Verificando configuración de puertos..."
echo ""

# Verificar puertos
echo "📡 PUERTOS DEL SISTEMA:"
echo "   FastAPI (API Backend): 8000"
echo "   Streamlit (Dashboard): 8501"
echo ""

# Verificar si los puertos están en uso
echo "🔍 VERIFICANDO PUERTOS EN USO:"

# Puerto 8000 (API)
if netstat -an | grep -q ":8000"; then
    echo "   ✅ Puerto 8000: EN USO (API probablemente corriendo)"
else
    echo "   ❌ Puerto 8000: LIBRE (API no está corriendo)"
fi

# Puerto 8501 (Streamlit)  
if netstat -an | grep -q ":8501"; then
    echo "   ✅ Puerto 8501: EN USO (Streamlit probablemente corriendo)"
else
    echo "   ❌ Puerto 8501: LIBRE (Streamlit no está corriendo)"
fi

echo ""

# Verificar conectividad del API
echo "🌐 VERIFICANDO CONECTIVIDAD DEL API:"
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "   ✅ API responde en http://localhost:8000/"
    
    # Verificar endpoint de docs
    if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
        echo "   ✅ Documentación disponible en http://localhost:8000/docs"
    else
        echo "   ⚠️ Documentación no accesible"
    fi
else
    echo "   ❌ API no responde en http://localhost:8000/"
    echo "      💡 Ejecuta: uv run uvicorn api.main:app --host 0.0.0.0 --port 8000"
fi

echo ""

# Verificar Dashboard
echo "🎨 VERIFICANDO DASHBOARD:"
if curl -s http://localhost:8501/ > /dev/null 2>&1; then
    echo "   ✅ Dashboard responde en http://localhost:8501/"
else
    echo "   ❌ Dashboard no responde en http://localhost:8501/"
    echo "      💡 Ejecuta: uv run streamlit run scripts/visualizations/main.py"
fi

echo ""

# Verificar variables de entorno
echo "🔧 VARIABLES DE ENTORNO:"
if [ -n "$API_URL" ]; then
    echo "   API_URL = $API_URL"
else
    echo "   API_URL = (no configurada, usando default local)"
fi

if [ -n "$STREAMLIT_RUNTIME_ENV" ]; then
    echo "   STREAMLIT_RUNTIME_ENV = $STREAMLIT_RUNTIME_ENV"
else
    echo "   STREAMLIT_RUNTIME_ENV = (no configurada)"
fi

echo ""

# Verificar archivos de configuración
echo "📁 ARCHIVOS DE CONFIGURACIÓN:"
if [ -f ".streamlit/secrets.toml" ]; then
    echo "   ✅ .streamlit/secrets.toml existe"
else
    echo "   ⚠️ .streamlit/secrets.toml no encontrado"
fi

if [ -f "pyproject.toml" ]; then
    echo "   ✅ pyproject.toml existe"
else
    echo "   ❌ pyproject.toml no encontrado"
fi

if [ -f "Dockerfile" ]; then
    echo "   ✅ Dockerfile existe"
else
    echo "   ❌ Dockerfile no encontrado"
fi

echo ""
echo "🎯 COMANDOS ÚTILES:"
echo "   Levantar API:       uv run uvicorn api.main:app --host 0.0.0.0 --port 8000"
echo "   Levantar Dashboard: uv run streamlit run scripts/visualizations/main.py"
echo "   Ver puertos:        netstat -ano | grep -E ':(8000|8501)'"
echo "   Matar proceso:      kill \$(lsof -t -i:8000)"
echo ""
echo "📋 Para más detalles: ENVIRONMENT_CONFIG.md"