import pandas as pd
import os

class SaveCleanData():

    def save(self, dataframe: pd.DataFrame, dataframe_name):

        # Get the root path of the project

        project_root = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "../.."
        ))

        # Define the new directory name where it will be set all the new
        # cleaned data

        output_dir = os.path.join(project_root, "output", "cleaned_data")

        # Here it'll create the new files based on the dataframe name

        processed_data_path = os.path.join(
            output_dir,
            f"{dataframe_name}.csv"
        )

        try:
            print("Guardando el archivo final limpio")

            # Create the output directory
            os.makedirs(
                output_dir, exist_ok=True
            )

            # Transform the clean dataframes to csv files
            dataframe.to_csv(processed_data_path, index=False)

            return processed_data_path

        except Exception as e:

            print(f"Error al guardar los datos {e}")

            return False

