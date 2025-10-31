import pandas as pd
import streamlit as st
import os

class DataManager:

    @st.cache_data
    def load_data(self, dataset_name):

        # Get the root path of the project
        project_root = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "../.."
        ))

        # Get the directory route where is the dataset
        dataset_dir = os.path.join(project_root, "output/cleaned_data")

        # Create the path to the file
        data_path= os.path.join(
            dataset_dir,
            f"{dataset_name}.csv"
        )

        # Check if the file exist, if it doesn't throw an exception with raise
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"No se encontro el archivo {data_path}")

        try:

            dataframe = pd.read_csv(data_path)

            return dataframe

        except Exception as e:

            st.error(f"Error al cargar los datos: {e}")

            return None

    # First step we normalize the names of the columns, by first deleting all
    # the extra spaces in the word, then changing the spaces for underscores,
    # and removing all the acentuations

    def normalize_columns(self, dataframe: pd.DataFrame):
        
        dataframe.columns = (
            dataframe.columns.str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("á", "a")
            .str.replace("é", "e")
            .str.replace("í", "i")
            .str.replace("ó", "o")
            .str.replace("ú", "u")
        )

        return dataframe
    
    def filter_by_category(self, category_name):

        INDICADORES_BALANCE = {
            "FONDOS DISPONIBLES": "Liquidez inmediata",
            "INVERSIONES": "Activos financieros",
            "CARTERA DE CRÉDITOS": "Préstamos otorgados",
            "DEUDORES POR ACEPTACIONES": "Compromisos de pago",
            "CUENTAS POR COBRAR": "Cuentas pendientes",
            "PROPIEDADES Y EQUIPO": "Activos fijos",
            "OTROS ACTIVOS": "Activos diversos"
        }

        INDICADORES_RENDIMIENTO = {
            "RESULTADOS DEL EJERCICIO / ACTIVO PROMEDIO": "ROA - Rentabilidad",
            "RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO": "ROE - Rentabilidad",
            "MOROSIDAD DE LA CARTERA TOTAL": "Calidad de cartera",
            "ACTIVOS PRODUCTIVOS / TOTAL ACTIVOS": "Eficiencia activos",
            "FONDOS DISPONIBLES / TOTAL DEPOSITOS A CORTO PLAZO": "Liquidez",
            "GASTOS DE OPERACION ESTIMADOS / TOTAL ACTIVO PROMEDIO (3)": "Eficiencia operativa"
        }

        INDICADORES_ESTRUCTURA = {
            "TOTAL ACTIVO": "Tamaño del banco",
            "TOTAL PATRIMONIO": "Capital propio",
            "TOTAL PASIVOS": "Obligaciones totales",
            "OBLIGACIONES CON EL PÚBLICO": "Depósitos captados",
            "CAPITAL SOCIAL": "Capital accionario"
        }
        # To make this we need the dataframe, the dictionary of the indicadores,
        # where we're going to take only the keys and turn it into a list
        # then take only the rows that has the list of indicadores

        if category_name== "Balance":
            indicadores_activos = INDICADORES_BALANCE
            es_porcentaje = False
            unidad = "$"
            st.info("💼 **Balance:** Activos y recursos del banco")
        elif category_name== "Rendimiento":
            indicadores_activos = INDICADORES_RENDIMIENTO
            es_porcentaje = True
            unidad = "%"
            st.info("📊 **Rendimiento:** Rentabilidad y eficiencia")
        else:
            indicadores_activos = INDICADORES_ESTRUCTURA
            es_porcentaje = False
            unidad = "$"
            st.info("🏗️ **Estructura:** Composición financiera")
