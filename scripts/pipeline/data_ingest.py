import os

class DataIngester:

    def ingest (self, dataset_name):

        # Get the path of the current script 
        file_path= os.path.dirname(os.path.abspath(__file__))

        # Builds up the path to the dataset
        data_path= os.path.join(file_path, r"..\..", dataset_name,
                                f"{dataset_name}.xlsx")

        # Check if the file exist, if it doesn't throw an exception with raise
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"No se encontro el archivo {data_path}")

        return data_path 

