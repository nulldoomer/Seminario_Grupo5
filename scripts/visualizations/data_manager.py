from typing import Optional
import pandas as pd
import streamlit as st
import os
from indicator_config import IndicatorConfig

class DataManager:


    def __init__(self, data_loader):

        self.load_data = data_loader

        self.dataframe : Optional[pd.DataFrame] = None

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


    # def filter_by_category( self, category, is_percentage):
    #
    #     indicator_names = IndicatorConfig.get_indicator_names_by_category(
    #         category
    #     )
    #
    #     filtered_dataframe = self.dataframe[
    #         self.dataframe["nombre_del_indicador"].isin(
    #             indicator_names.keys()
    #         )
    #     ].copy()
    #
    #     return filtered_dataframe
    #
    #
