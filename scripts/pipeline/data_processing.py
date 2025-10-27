import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class CreateDataframes:

    def create(self, dataset_path):

        # Create the dataframes for the data we previously analysed

        sheet_names = [
            "BALANCE", "BALANCE %",
            "COMPOS CART","COMPOS CART %",
            "INDICADORES"
        ]

        dataframe_dict = {}

        # Fill the dictionary with the dataframes
        # And use the first strategy to clean the data, skiping the rows
        # and using only the columns of the table

        for sheet in sheet_names:
            temp_dataframe = pd.read_excel(dataset_path, sheet_name= sheet,
                                           skiprows=7)
            dataframe_dict[sheet] = temp_dataframe

        # Return all the dataframes created

        return dataframe_dict


# We inherit from BaseEstimator and TransformerMixin to make this class 
# compatible with sklearn Pipelines. These base classes ensure that our custom 
# transformer implements the required fit() and transform() methods,
# allowing sklearn to call fit_transform() and integrate this step seamlessly 
# into a data processing workflow.

class DropBlankColumns(BaseEstimator, TransformerMixin):

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

        X.drop("Unnamed: 0", axis=1, inplace=True)

        X = X.reset_index(drop=True)

        return X 



class DropRowsWithoutValues(BaseEstimator, TransformerMixin):

    def fit(self, X: pd.DataFrame, y=None):

        return self

    def transform(self, X: pd.DataFrame):

        X = X.copy()

        # Drop the rows that have the definition and name, but it doesn't 
        # have values at all on the banks columns
        # We'll be looking to rows with 3 values at most to keep, because the
        # ones that only has the 2 are the ones without bank values

        # Also drops all the rows that doesn't have at least one value, which 
        # is totally usefull because we don't want blank insertions in our db
        
        X.dropna(thresh=3, inplace=True)

        X = X.reset_index(drop=True)

        return X


# Processing for Balance Dataframe

class TakePriorRows(BaseEstimator, TransformerMixin):

    def fit(self, X: pd.DataFrame, y=None):

        return self

    def transform(self, X: pd.DataFrame):

        X = X.copy()

        # Keep only the rows where the code is less than 100, because there
        # are the most significants rows, the other ones doesn't matter

        X["CÓDIGO"] = pd.to_numeric(X["CÓDIGO"], errors="coerce")

        X = X.loc[X["CÓDIGO"] < 100].copy()

        X = X.reset_index(drop=True)

        return X
