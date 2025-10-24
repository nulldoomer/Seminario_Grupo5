from data_ingest import DataIngester
from data_processing import CreateDataframes

from data_pipeline import (
    CleaningPipeline,
    BalanceCleaningPipeline
)

def main():

    # Creating the instances of the classes

    ingester = DataIngester()
    dataframe_creator = CreateDataframes()
    main_pipeline = CleaningPipeline()
    balance_pipeline = BalanceCleaningPipeline()
    dataset_name = "dataset"

    try:
        # Load the file
        path = ingester.ingest(dataset_name)
        print(f"Ruta del archivo cargado {path}")

        # Create the dataframes
        dataframes = dataframe_creator.create(path)

        for name, df in dataframes.items():

            print(f"\nProcesando hoja: {name}")

            if "BALANCE" == name:

                print("→ Aplicando pipeline de BALANCE")
                df = balance_pipeline.clean(df)

            else:

                 print("→ Aplicando pipeline general")
                 df = main_pipeline.clean(df)


            print("Resultado después del pipeline:")
            print(df.head(5))
            print(f"Shape final: {df.shape}")
            # print(f"Check de Columnas: {df.dtypes}")

    except FileNotFoundError as e:

        print(e)







if __name__ == "__main__":
    main()



