import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class CreateDataframes:

    def create(self, dataset_path):

        # Create the dataframes for the data we previously analysed

        dataframe_dict = {}
        sheet_names = [
            "BALANCE", "BALANCE %",
            "COMPOS CART","COMPOS CART %",
            "INDICADORES"
        ]

        # Fill the dictionary with the dataframes
        # And use the first strategy to clean the data, skiping the rows
        # and using only the columns of the table

        for sheet in sheet_names:
            temp_dataframe = pd.read_excel(dataset_path, sheet_name= sheet,
                                           skiprows=7)
            dataframe_dict[sheet] = temp_dataframe

        # Create each one of the dataframes from the dictionary

        dataframe_balance = dataframe_dict["BALANCE"]
        dataframe_balance_ptj = dataframe_dict["BALANCE %"]
        dataframe_composcart = dataframe_dict["COMPOS CART"]
        dataframe_composcart_ptj = dataframe_dict["COMPOS CART %"]
        dataframe_indicadores = dataframe_dict["INDICADORES"]

        # Return all the dataframes created

        return (dataframe_balance, dataframe_balance_ptj, dataframe_composcart,
                dataframe_composcart_ptj, dataframe_indicadores)



class DataCleaning(BaseEstimator, TransformerMixin):

    def fit(self, X: pd.DataFrame, y= None):

        return self


    def transform(self, X: pd.DataFrame):
        # Drop the blank column which is in all the dataframes
        # axis specifies that is a column and inplace mute the same object
        # also use errors=ignore to avoid exceptions if the column doesn't 
        # exist in the dataframe

        # But I know that ain't gonna happen because i saw all the excel
        # and its all the same in the tables we use

        X = X.copy()

        X.drop("BANCOS PRIVADOS VIVIENDA", axis=1, inplace=True,
                       errors="ignore")

        return X 


