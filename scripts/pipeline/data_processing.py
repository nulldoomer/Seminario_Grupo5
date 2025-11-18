import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class CreateDataframes:

    def create(self, dataset_path):

        # Create the dataframes for the data we previously analysed

        sheet_names = [
            "BALANCE", 
            "COMPOS CART",
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

# We change the format of the dataframes, because it's wide and complex to
# analyse so we're changing that by using melt function to it and returning
# the melted dataframe, so now we have 3 columns with every record of every
# bank

class MeltBanksIndicatorsAndValues(BaseEstimator, TransformerMixin):

    def fit(self, X:pd.DataFrame, y=None):

        return self


    # Because the format of the tables are not the same we apply a filter to
    # change the dataframe and mantain the flow of information on this ones

    def transform(self, X: pd.DataFrame):
        
        X = X.copy()

        if "CUENTA" in X.columns:

            id_cols = ["CÓDIGO","CUENTA"]

        elif "NOMBRE DEL INDICADOR" in X.columns:

            id_cols = ["NOMBRE DEL INDICADOR"]

        else:
            return Exception(f"No se encontro la columna con ese nombre")


        # We use the column that'll be the same, with id_col after we checked
        # the value of it
        X_melted = pd.melt(
            X,
            id_vars= id_cols,
            var_name= "Banks",
            value_name="Valor Indicador"
        ).copy()

        return X_melted

# After we filter and clean the data, we drop the unused column of CÓDIGO

class DropCodeColumn(BaseEstimator, TransformerMixin):

    def fit(self, X: pd.DataFrame, y=None):

        return self

    def transform(self, X: pd.DataFrame):

        X = X.copy()

        X.drop("CÓDIGO", axis=1, inplace=True,
               errors="ignore")

        X = X.reset_index(drop=True)

        return X 


# After we match the number of columns on each dataframe, we continue with
# changing the name to match everything for the concat of the dataframes

class RenameColumns(BaseEstimator, TransformerMixin):

    def fit(self, X: pd.DataFrame, y=None):

        return self

    def transform(self, X: pd.DataFrame):

        X = X.copy()

        X.rename(columns={"CUENTA": "NOMBRE DEL INDICADOR"}, inplace=True)

        return X

# Finally after cleaning and matching all the main data, we concat all the
# dataframes into big tidy one

class ConcatDataframes(BaseEstimator, TransformerMixin):

    def fit(self, X: pd.DataFrame, y=None):

        return self

    def transform(self, X:(pd.DataFrame)):

        X = X.copy()

        X_final_dataframe = pd.concat(X)

        return X_final_dataframe


# FILTRO DE CATEGORÍAS BANCARIAS
class FilterRealBanks(BaseEstimator, TransformerMixin):
    """
    Filtrar solo bancos reales, eliminar categorías de clasificación.
    Estas categorías son agrupaciones de la Superintendencia de Bancos,
    NO son instituciones bancarias individuales.
    """

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame):
        X = X.copy()

        # Categorías a excluir (NO son bancos individuales)
        categories_to_exclude = {
            'BANCA MÚLTIPLE',
            'BANCOS PRIVADOS COMERCIALES', 
            'BANCOS PRIVADOS CONSUMO',
            'BANCOS PRIVADOS GRANDES',
            'BANCOS PRIVADOS MEDIANOS', 
            'BANCOS PRIVADOS MICROCRÉDITO',
            'BANCOS PRIVADOS PEQUEÑOS',
            'TOTAL BANCOS PRIVADOS'
        }

        # Verificar si existe la columna 'Banks'
        if 'Banks' in X.columns:
            initial_count = len(X)
            initial_banks = X['Banks'].nunique()
            
            # Filtrar las categorías
            X_filtered = X[~X['Banks'].isin(categories_to_exclude)].copy() #type:ignore
            
            final_count = len(X_filtered)
            final_banks = X_filtered['Banks'].nunique()#type:ignore
            
            print(f"Filtro de categorías bancarias aplicado:")
            print(f"   Registros: {initial_count} → {final_count}")
            print(f"   Entidades: {initial_banks} → {final_banks}")
            print(f"   Categorías eliminadas: {initial_banks - final_banks}")
            
            return X_filtered
        else:
            print("Columna 'Banks' no encontrada, devolviendo datos sin filtrar")
            return X

