from sklearn.pipeline import Pipeline

from data_processing import  (
    DropBlankColumns, 
    DropRowsWithoutValues,
    TakePriorRows,
    MeltBanksIndicatorsAndValues,
    DropCodeColumn,
    RenameColumns,
    ConcatDataframes,
    FilterRealBanks  
)

class CleaningPipeline:

    def clean(self, dataframe):
        
        # Execute the process in sequence, obtain the result from one process
        # and use that result to continue with the other one

        cleaning_pipe = Pipeline([
            ("blank_column_dropper", DropBlankColumns()),
            ("row_dropper", DropRowsWithoutValues()),
            ("tidy_formatter", MeltBanksIndicatorsAndValues()),
            ("real_banks_filter", FilterRealBanks())
        ])

        transformed_dataframe = cleaning_pipe.fit_transform(dataframe)

        return transformed_dataframe


# Apply inheritance because we want to mantain the main processing but
# we want to take specific rows because on this dataframe there is a big lack 
# of information and no needed one

class BalanceCleaningPipeline(CleaningPipeline):

    def clean(self, dataframe):

        # Apply the base pipeline for cleaning the data

        transformed_dataframe = super().clean(dataframe)

        # Implement the new specific pipeline for the dataframe

        balance_pipe = Pipeline([
            ("row_picker", TakePriorRows())
        ])

        final_dataframe = balance_pipe.fit_transform(
            transformed_dataframe
        )

        return final_dataframe 

class MatchColumnsPipeline:

    def match(self, dataframe):

        match_pipe = Pipeline([
            ("drop_extra_column", DropCodeColumn()),
            ("rename_columns", RenameColumns())
        ])

        transformed_dataframe = match_pipe.fit_transform(dataframe)

        return transformed_dataframe

class ConcatDataframesPipeline:

    def concat(self, dataframe):

        concat_pipe= Pipeline([
            ("concater", ConcatDataframes())
        ])

        transformed_dataframe = concat_pipe.fit_transform(dataframe)

        return transformed_dataframe


# PIPELINE DE FILTRADO DE BANCOS REALES
class BankFilterPipeline:
    """Pipeline para filtrar categorías bancarias y dejar solo bancos reales"""
    
    def filter(self, dataframe):
        """
        Aplicar filtro de bancos reales al dataframe final
        """
        print("\n🧹 Aplicando filtro de bancos reales...")
        
        filter_pipe = Pipeline([
        ])
        
        filtered_dataframe = filter_pipe.fit_transform(dataframe)
        
        print("✅ Filtro de bancos reales completado")
        return filtered_dataframe
