from data_ingest import DataIngester
from data_processing import CreateDataframes
from data_pipeline import CleaningPipeline

def main():

    ingester = DataIngester()
    dataframe_creator = CreateDataframes()
    pipeline = CleaningPipeline()
    dataset_name = "dataset"

    try:
        path = ingester.ingest(dataset_name)
        print(f"Ruta del archivo cargado {path}")

        data_frames = dataframe_creator.create(path)

        for df in data_frames:
            pipeline.clean(df)
            print(f" Dataframe {df}")

    except FileNotFoundError as e:
        print(e)







if __name__ == "__main__":
    main()



