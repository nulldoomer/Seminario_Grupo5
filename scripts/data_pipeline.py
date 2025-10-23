from sklearn.pipeline import Pipeline
from data_processing import  DropBlankColumn, DropRowsWithoutValues

class CleaningPipeline:

    def clean(self, dataframe):
        
        # Execute the process in sequence, obtain the result from one process
        # and use that result to continue with the other one

        cleaning_pipe= Pipeline([
            ("blank_column_dropper", DropBlankColumn()),
            ("row_dropper", DropRowsWithoutValues())
        ])

        transformed_dataframe = cleaning_pipe.fit_transform(dataframe)

        return transformed_dataframe
