import os
import pandas as pd

# Ruta absoluta de la carpeta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "dataset", "dataset.xlsx")


def load_data(path):
    print(f" Cargando datos desde {path}")

    try:
        df = pd.read_excel(path)
        print("Datos han sido cargados")
        return df
    except FileNotFoundError:
        print(f" Error: no se encontro el archivo en {path}")
        print("Asegurate de tener el archivo cargado")

        return None
    except Exception as e:
        print(f"Ocurrio un error inesperado {e}")
        return None


if __name__ == "__main__":
    # indica dónde está el script actual
    print(f"Ejecutando script desde: {os.path.abspath(__file__)}")

    # llama a la función de arriba para cargar el csv
    dataframe_juegos = load_data(DATA_PATH)

    if dataframe_juegos is not None:
        print("\n---Primeras 5 filas---")
        print(dataframe_juegos.head())

        print("\n---Información del DataFrame---")
        dataframe_juegos.info()
