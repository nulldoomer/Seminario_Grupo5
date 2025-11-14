"""
🧪 Dashboard de Prueba - Conexión API
Test simple para verificar conexión
"""
import streamlit as st
import sys
from pathlib import Path

# Agregar path para imports
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

try:
    from services.api_client import get_api_client
    
    st.set_page_config(
        page_title="Test API Connection",
        page_icon="🧪",
        layout="wide"
    )
    
    st.title("🧪 Test de Conexión API")
    st.markdown("---")
    
    # Obtener cliente API
    api_client = get_api_client()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**URL del API:** `{api_client.base_url}`")
    
    with col2:
        if st.button("🔄 Probar Conexión"):
            st.rerun()
    
    st.markdown("---")
    
    # Test 1: Lista de bancos
    st.subheader("📊 Test 1: Lista de Bancos")
    try:
        with st.spinner("Cargando bancos..."):
            bancos = api_client.get_banks_list("Balance")
        
        if bancos:
            st.success(f"✅ {len(bancos)} bancos encontrados")
            st.write("Primeros bancos:", bancos[:5])
        else:
            st.error("❌ No se pudieron cargar los bancos")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
    
    st.markdown("---")
    
    # Test 2: Indicadores
    st.subheader("📈 Test 2: Lista de Indicadores")
    categoria_test = st.selectbox("Categoría:", ["Balance", "Rendimiento", "Estructura"])
    
    try:
        with st.spinner("Cargando indicadores..."):
            indicators_data = api_client.get_indicators_list(categoria_test)
        
        if indicators_data:
            indicadores = indicators_data.get("indicators", [])
            st.success(f"✅ {len(indicadores)} indicadores encontrados para {categoria_test}")
            st.write("Indicadores:", indicadores)
        else:
            st.error("❌ No se pudieron cargar los indicadores")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
    
    st.markdown("---")
    
    # Test 3: Datos de banco (si hay bancos disponibles)
    if 'bancos' in locals() and bancos:
        st.subheader("🏦 Test 3: Datos de Banco")
        banco_test = st.selectbox("Banco:", bancos[:5])
        
        if st.button("Cargar Datos del Banco"):
            try:
                with st.spinner(f"Cargando datos de {banco_test}..."):
                    bank_response = api_client.get_bank_financials(banco_test, categoria_test)
                
                if bank_response:
                    st.success("✅ Datos del banco cargados exitosamente")
                    st.json(bank_response)
                else:
                    st.error("❌ No se pudieron cargar los datos del banco")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.markdown("---")
    st.info("💡 Si ves errores de conexión, verifica que el API esté corriendo en el puerto correcto")

except ImportError as e:
    st.error(f"❌ Error de importación: {e}")
    st.info("Asegúrate de que el archivo `services/api_client.py` existe")
except Exception as e:
    st.error(f"❌ Error general: {e}")
    import traceback
    st.code(traceback.format_exc())