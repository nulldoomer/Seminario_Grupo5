import pandas as pd
import os

def test_csv_loading():
    """Test que verifica que el CSV se carga correctamente"""
    # Obtener la ruta del directorio del script actual
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construir la ruta hacia el archivo CSV desde la ubicación del script
    csv_path = os.path.join(script_dir, "..", "..", "output", "cleaned_data", "Final Dataframe.csv")
    # Normalizar la ruta para resolver los '..'
    csv_path = os.path.normpath(csv_path)
    
    print(f"🔍 Ruta construida: {csv_path}")
    print(f"📁 ¿Existe el archivo?: {os.path.exists(csv_path)}")
    
    try:
        df = pd.read_csv(csv_path)
        print(f"✅ Archivo cargado exitosamente!")
        print(f"📊 Forma del DataFrame: {df.shape}")
        print(f"📋 Columnas: {list(df.columns)}")
        print(f"🏦 Bancos únicos: {df['Banks'].nunique()}")
        print(f"📈 Indicadores únicos: {df['NOMBRE DEL INDICADOR'].nunique()}")
        print(f"\n🔢 Primeras 3 filas:")
        print(df.head(3))
        return True
    except Exception as e:
        print(f"❌ Error al cargar el archivo: {e}")
        return False

if __name__ == "__main__":
    test_csv_loading()