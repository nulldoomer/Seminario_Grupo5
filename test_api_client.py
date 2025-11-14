"""
Test directo del API Client
"""
import sys
from pathlib import Path

# Agregar path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

try:
    from scripts.visualizations.services.api_client import get_api_client
    
    print("🔧 Probando API Client...")
    api_client = get_api_client()
    print(f"✅ Cliente creado con URL: {api_client.base_url}")
    
    # Test simple - solo mostrar que se puede importar
    print("📋 Métodos disponibles:")
    methods = [method for method in dir(api_client) if not method.startswith('_')]
    for method in methods:
        print(f"  - {method}")
    
    print("\n✅ API Client importado exitosamente!")
    print("ℹ️ Para conectar con el API, asegúrate de que esté corriendo en el puerto correcto")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()