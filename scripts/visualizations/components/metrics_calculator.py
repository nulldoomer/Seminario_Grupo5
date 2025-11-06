import pandas as pd

class MetricsCalculator:

    @staticmethod
    def calculate_total(
        df: pd.DataFrame,
        column: str = "valor_indicador"
    ):
        
        if column not in df.columns:
            return 0.0
        
        return float(df[column].sum())

    @staticmethod
    def calculate_average(
        df: pd.DataFrame,
        column : str = "valor_indicador"
    ):
        if column not in df.columns:
            return 0.0

        return float(df[column].mean())

    @staticmethod
    def get_top_n(
        df: pd.DataFrame,
        n: int = 3,
        column : str = "valor_indicador"
    ):
        
        if column not in df.columns or df.empty:
            return pd.DataFrame()

        return df.nlargest(n,column)


    @staticmethod
    def get_bottom_n(
        df: pd.DataFrame,
        n: int = 3,
        column : str = "valor_indicador"
    ):
        
        if column not in df.columns or df.empty:
            return pd.DataFrame()

        return df.nsmallest(n,column)

    # Get the max indicator with it own value
    @staticmethod
    def get_max_indicator(df: pd.DataFrame):

        if df.empty or "valor_indicador" not in df.columns or "nombre_del_indicador" not in df.columns:
            return ("", 0.0)

        # Get the id on the dataframe based on the max value of the column
        # valor_indicador, and then get the row with .loc
        max_idx = df["valor_indicador"].idxmax()
        max_row = df.loc[max_idx]

        return (
            str(max_row["nombre_del_indicador"]),
            float(max_row["valor_indicador"])
        )

    # Get the min indicator with it own value
    @staticmethod
    def get_min_indicator(df: pd.DataFrame):


        if df.empty or "valor_indicador" not in df.columns or "nombre_del_indicador" not in df.columns:
            return ("", 0.0)

        min_idx= df["valor_indicador"].idxmin()
        min_row= df.loc[min_idx]

        return (
            str(min_row["nombre_del_indicador"]),
            float(min_row["valor_indicador"])
        )

    # Get a dictionary of the sumary of statistics of the dataframe
    @staticmethod
    def get_sumary_stats(df: pd.DataFrame):
        
        if df.empty or "valor_indicador" not in df.columns:
            return {
                "total": 0.0,
                "promedio": 0.0,
                "mediana": 0.0,
                "desviacion": 0.0,
                "min": 0.0,
                "max": 0.0
            }

        return{
            "total" : float(df["valor_indicador"].sum()),
            "promedio" : float(df["valor_indicador"].mean()),
            "mediana" : float(df["valor_indicador"].median()),
            "desviacion" : float(df["valor_indicador"].std()),
            "min" : float(df["valor_indicador"].min()),
            "max" : float(df["valor_indicador"].max()),
        }
