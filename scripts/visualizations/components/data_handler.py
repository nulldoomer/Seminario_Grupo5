from typing import Any, Dict, List, Optional
import pandas as pd
import streamlit as st
from ..data_loader import VisualizationDataLoader

class DataHandler:


    def __init__(self, data_loader: VisualizationDataLoader):

        self.data_loader = data_loader

        self.dataframe : Optional[pd.DataFrame] = None

    def load_data(self, dataset_name)-> Optional[pd.DataFrame]:

        try:

            path = self.data_loader.load(dataset_name)
            dataframe = pd.read_csv(path)
            self.dataframe = self.normalize_columns(dataframe)

            return self.dataframe

        except Exception as e:
            st.error(f"Error al cargar los datos{e}")

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


    # Filter the dataframe by category, so we return a dataframe from the
    # original that only has the all the indicators by that category

    def filter_by_category(
        self, 
        indicator_names: Dict[str, str],
        convert_percentage: bool = False
    ) -> pd.DataFrame:

        # Check if it's None
        if self.dataframe is None:
            st.error("No hay datos cargados. Ejecuta load_data() primero.")
            return pd.DataFrame()

        # Give an error if the indicator doesn't exists on the dataframe
        if "nombre_del_indicador" not in self.dataframe.columns:
            st.error(" La columna 'nombre_del_indicador' no existe")
            return pd.DataFrame()

        # Turn the dictionary keys into a list
        indicator_list = list(indicator_names.keys())

        # Create the filter so then apply the filter to the dataframe
        mask = self.dataframe["nombre_del_indicador"].isin(indicator_list)
        df_filtered = self.dataframe[mask].copy()

        # Check if the instance exists
        if not isinstance(df_filtered, pd.DataFrame):
            return pd.DataFrame()

        if convert_percentage and not df_filtered.empty:
            df_filtered = self.convert_to_percentage(df_filtered)

        return df_filtered



    # Transform all the decimal values to representative percentage

    @staticmethod
    def convert_to_percentage(df: pd.DataFrame) -> pd.DataFrame:

        df_result = df.copy()
        if "valor_indicador" in df_result.columns:
            df_result["valor_indicador"] = df_result["valor_indicador"] * 100
        return df_result


    # We use this to transform the tidy form to wide form to get the values 
    # of every indicator by bank, and then apply this to create a chart with 
    # the values of every indicator by a single bank

    def get_pivot_table(
        self,
        df: pd.DataFrame,
        indicator_order: List[str] 
    ):

        pivot = df.pivot_table(
            index="banks",
            columns="nombre_del_indicador",
            values="valor_indicador",
            aggfunc="mean"
        )

        # Re-order the columns if it's specified
        if indicator_order:

            available_cols = [col for col in indicator_order if col in pivot]
            pivot = pivot[available_cols]

        return pivot

    
    # Get the ranking of banks by specific indicator, so we can get a general
    # chart where we'll see the best and worst bank in ascending order

    def get_ranking(
        self,
        df: pd.DataFrame,
        indicator : str,
        ascending: bool = False
    ):
        if "nombre_del_indicador" not in df.columns or "valor_indicador" not in df.columns:
            st.error("Faltan columnas requeridas")
            return pd.DataFrame()
        
        ranking = df[df["nombre_del_indicador"] == indicator].copy() # type: ignore
        
        if ranking.empty:
            st.warning(f"No hay datos para el indicador: {indicator}")
            return pd.DataFrame()
        
        ranking: pd.DataFrame = ranking.sort_values(
            by='valor_indicador',
            ascending=ascending
        ).reset_index(drop=True)

        # Start from 1
        ranking.index = ranking.index + 1
        
        return ranking

    
    # Get all the indicators from a bank, get the names and the values 

    def get_bank_data(
        self,
        df: pd.DataFrame,
        bank_name: str,
        sort_by_value: bool=True
    ):

        bank_df = df[df["banks"] == bank_name].copy() # type:ignore

        if sort_by_value and not bank_df.empty:

            bank_df: pd.DataFrame = bank_df.sort_values(
                by="valor_indicador", ascending=False
            )
        
        return bank_df


    def get_unique_values(self, df: pd.DataFrame, column: str) -> List[str]:
            """
            Obtiene valores únicos de una columna
            
            Args:
                df: DataFrame
                column: Nombre de la columna
            
            Returns:
                Lista de valores únicos ordenados
            """
            if column not in df.columns:
                st.warning(f"La columna '{column}' no existe")
                return []
            
            return sorted(df[column].unique().tolist())

    def get_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Obtiene resumen del DataFrame
        
        Args:
            df: DataFrame a resumir
        
        Returns:
            Diccionario con información resumida
        """
        summary = {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "total_banks": df["banks"].nunique() if "banks" in df.columns else 0,
            "total_indicators": df["nombre_del_indicador"].nunique() if "nombre_del_indicador" in df.columns else 0
        }
        return summary
