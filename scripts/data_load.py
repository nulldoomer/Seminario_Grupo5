import os
import missingno as msno
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
    df_bancos= load_data(DATA_PATH)


    if df_bancos is not None:

        valores_unicos =  df_bancos.nunique()
        valores_nulos = df_bancos.isnull().sum()

        print("##############################################################")
        print("\n---Primeras 5 filas---")
        print(df_bancos.head())
        print("##############################################################")

        print("\n---Información del DataFrame---")
        print("##############################################################")
        df_bancos.info()

        print(df_bancos.columns)
        print("##############################################################")

        datos_generales = pd.DataFrame({
            "V_U": valores_unicos,
            "V_Null": valores_nulos
        })

        print("##############################################################")

        print(datos_generales)

        print("##############################################################")
        # Distribucion de valores nulos por porcentaje

        pctj_nulls = round(df_bancos.isnull().mean() * 100,3)

        print("##############################################################")
        print(pctj_nulls)

        # Matriz para ver donde estan los valores nulos
        # Puede representar graficos con data frames
        # una matriz, heatmap de correlacion, etc
        print(msno.matrix(df_bancos))

        # Frecuencia o distribucion de los datos

        print("##############################################################")
        for i in df_bancos.columns:
            print(f"Se enseña la columna {i}")
            print(df_bancos[i].value_counts(normalize=True)*100)
            print("")
        
        #Tipos de datos del dataframe
        print("##############################################################")
        print(df_bancos.dtypes)

        # Resumen Estadistico
        print(df_bancos.describe())
