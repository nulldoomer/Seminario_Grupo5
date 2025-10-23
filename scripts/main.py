from data_ingest import DataIngester

def main():

    ingester = DataIngester()
    dataset_name = "dataset"

    try:

        path = ingester.ingest(dataset_name)
        print(f"Ruta del archivo cargado {path}")

    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()



