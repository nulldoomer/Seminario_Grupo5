from sklearn.pipeline import Pipeline

from data_processing import  (
    DropBlankColumns, 
    DropRowsWithoutValues,
    TakePriorRows
)

class CleaningPipeline:

    def clean(self, dataframe):
        
        # Execute the process in sequence, obtain the result from one process
        # and use that result to continue with the other one

        cleaning_pipe= Pipeline([
            ("blank_column_dropper", DropBlankColumns()),
            ("row_dropper", DropRowsWithoutValues())
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

        balance_pipe= Pipeline([
            ("row_picker", TakePriorRows())
        ])

        final_dataframe = balance_pipe.fit_transform(
            transformed_dataframe
        )

        return final_dataframe 

