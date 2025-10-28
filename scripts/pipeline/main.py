from data_ingest import DataIngester
from data_processing import CreateDataframes
from data_saving import SaveCleanData

from data_pipeline import (
    CleaningPipeline,
    BalanceCleaningPipeline,
    MatchColumnsPipeline,
    ConcatDataframesPipeline
)

def main():

    # Creating the instances of the classes

    ingester = DataIngester()
    dataframe_creator = CreateDataframes()
    main_pipeline = CleaningPipeline()
    balance_pipeline = BalanceCleaningPipeline()
    match_pipeline = MatchColumnsPipeline()
    concat_pipeline = ConcatDataframesPipeline()
    data_saver = SaveCleanData()
    dataset_name = "dataset"

    try:
        # Load the file
        path = ingester.ingest(dataset_name)
        print(f"Ruta del archivo cargado {path}")

        # Create the dataframes
        dataframes = dataframe_creator.create(path)

        final_dataframes = []

        for name, df in dataframes.items():

            print(f"\nProcesando hoja: {name}")

            if name == "BALANCE":

                print("→ Aplicando pipeline de BALANCE")
                df = balance_pipeline.clean(df)
                df = match_pipeline.match(df)

            else:

                 print("→ Aplicando pipeline general")
                 df = main_pipeline.clean(df)
                 df = match_pipeline.match(df)

            print("Resultado después del pipeline:")
            print(df.head(5))
            print(f"Shape final: {df.shape}")

            final_dataframes.append(df)


        concat_dataframe = concat_pipeline.concat(final_dataframes)

        print("Resultado final:")
        print(concat_dataframe.head(5))
        print(f"Shape final: {concat_dataframe.shape}")
        data_saver.save(concat_dataframe, "Final Dataframe")

    except FileNotFoundError as e:

        print(e)




if __name__ == "__main__":
    main()



