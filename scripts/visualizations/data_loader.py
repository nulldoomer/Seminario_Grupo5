import os

class VisualizationDataLoader:

    def load(self, dataset_name):

        # Get the root path of the project
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

        return data_path 

