from sklearn.pipeline import Pipeline
from data_processing import  DataCleaning

class BancosPipeLine:

    def run(self, dataframe):
        
        banco_pipe = Pipeline([
            ("cleaner", DataCleaning())
        ])

        tf = banco_pipe.fit_transform(dataframe)

        return tf
