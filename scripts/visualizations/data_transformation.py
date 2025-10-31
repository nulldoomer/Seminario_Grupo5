import pandas as pd

# Transform the data from the csv to align to use it into the charts and
# graphs to reprensent it more easily

class TransformingDataForDashboard:

    # First step we normalize the names of the columns, by first deleting all
    # the extra spaces in the word, then changing the spaces for underscores,
    # and removing all the acentuations

    def column_normalizer(self, dataframe: pd.DataFrame):

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

    # Then we want only filter the data by some group of indicadores

    def indicadores_filter(self, dataframe: pd.DataFrame, indicadores_dict, is_percentage=False):

        # To make this we need the dataframe, the dictionary of the indicadores,
        # where we're going to take only the keys and turn it into a list
        # then take only the rows that has the list of indicadores

        indicadores_list = list(indicadores_dict.keys())

        filtered_dataframe = dataframe[dataframe["nombre_del_indicador"].isin(
            indicadores_list
        )].copy()

        # In a part of the union of the dataframes, there are values of the 
        # indicadores that are in float because its percentage values,
        # so we use our flag is_percentage and a check if its not empty
        # we take the values and we'll transform it into percentage multiplying
        # by 100 and return the data
        
        if is_percentage and not filtered_dataframe.empty:

            filtered_dataframe["valor_indicador"] = filtered_dataframe[
                "valor_indicador"
            ] * 100
        
        return filtered_dataframe 

