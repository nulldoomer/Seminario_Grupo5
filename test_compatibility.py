#!/usr/bin/env python3
"""
Script de verificación rápida para comprobar compatibilidad
de las dependencias y métodos de styling de pandas
"""

import pandas as pd
import numpy as np

def test_pandas_styling():
    """Prueba los métodos de styling que estamos usando"""
    print("🔍 Probando compatibilidad de pandas styling...")
    
    # Crear datos de prueba
    data = {
        'A': [1, 2, 3, 4],
        'B': [10, 20, 30, 40],
        'C': [-5, 0, 5, 10]
    }
    df = pd.DataFrame(data)
    
    try:
        # Probar background_gradient sin center
        styled1 = df.style.background_gradient(cmap='RdYlGn')
        print("✅ background_gradient(cmap='RdYlGn') - FUNCIONA")
        
        # Probar background_gradient con subset
        styled2 = df.style.background_gradient(subset=['C'], cmap='RdYlGn')
        print("✅ background_gradient(subset=['C'], cmap='RdYlGn') - FUNCIONA")
        
        # Probar format
        styled3 = df.style.format({'A': '{:.2f}%', 'B': '${:,.0f}'})
        print("✅ style.format() - FUNCIONA")
        
        # Probar set_properties
        styled4 = df.style.set_properties(**{'text-align': 'right'})
        print("✅ set_properties() - FUNCIONA")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en pandas styling: {e}")
        return False

def test_imports():
    """Prueba que todas las importaciones funcionan"""
    print("\n🔍 Probando importaciones...")
    
    try:
        import streamlit as st
        print("✅ streamlit - OK")
    except ImportError as e:
        print(f"❌ streamlit - ERROR: {e}")
        return False
    
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ plotly - OK")
    except ImportError as e:
        print(f"❌ plotly - ERROR: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✅ matplotlib - OK")
    except ImportError as e:
        print(f"❌ matplotlib - ERROR: {e}")
        return False
    
    return True

def main():
    print("🧪 VERIFICACIÓN DE COMPATIBILIDAD DEL DASHBOARD")
    print("=" * 50)
    
    # Información de la versión de pandas
    print(f"📋 Versión de pandas: {pd.__version__}")
    print(f"📋 Versión de numpy: {np.__version__}")
    
    # Probar importaciones
    imports_ok = test_imports()
    
    # Probar styling
    styling_ok = test_pandas_styling()
    
    print("\n📊 RESUMEN:")
    if imports_ok and styling_ok:
        print("✅ TODAS LAS PRUEBAS PASARON - Dashboard debería funcionar correctamente")
        print("\n🚀 Puedes ejecutar: streamlit run main.py")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
        if not imports_ok:
            print("   - Problema con importaciones")
        if not styling_ok:
            print("   - Problema con pandas styling")
    
    print("\n💡 Si hay errores, considera actualizar pandas:")
    print("   pip install pandas>=1.3.0")

if __name__ == "__main__":
    main()