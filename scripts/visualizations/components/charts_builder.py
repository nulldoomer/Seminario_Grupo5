from typing import Any, Tuple
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

class ChartBuilder:

    def __init__(self, is_percentage: bool=False, unit: str= "$"):

        self.is_percentage = is_percentage
        self.unit = unit

    def format_value(self, value: float):

        if self.is_percentage:

            return f"{value: .2f}%"
        else:

            return f"${value: .0f}"


    # Label all the bars from the chart of matplotlib, horizontal and vertical
    # values

    def add_value_labels(
        self,
        axis: Axes,
        bars: Any,
        horizontal: bool=True
    )-> None:
        for bar in bars:
            if horizontal:

                width = float(bar.get_width())
                y_pos = bar.get_y() + bar.get_height()/2

                axis.text(
                    width, y_pos,
                    self.format_value(width),
                    ha="left", va="center",
                    fontsize=8, fontweight='bold'
                )

            else:

                height = float(bar.get_height())
                x_pos = bar.get_x() + bar.get_width()/2

                axis.text(
                    x_pos, height,
                    self.format_value(height),
                    ha='center', va='bottom',
                    fontsize=8, fontweight='bold'
                )


    def create_horizontal_bar(
        self,
        df: pd.DataFrame,
        title: str,
        figsize: Tuple[int,int] = (12,6),
        color: str = "#2E86AB"
    )-> Figure:

        figure, axis = plt.subplots(figsize = figsize)

        bars = axis.barh(
            df["nombre_del_indicador"],
            df["valor_indicador"],
            color = color
        )

        self.add_value_labels(axis, bars, horizontal=True)

        axis.set_xlabel(f"Valor del Indicador({self.unit})", fontsize=11,
                        fontweight="bold")

        axis.set_title(title, fontsize=14, fontweight='bold', pad=20)
        axis.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        
        return figure
                        

    def create_ranking_chart(
        self,
        df: pd.DataFrame,
        title,
        figsize: Tuple[int, int] = (12, 8)
    )-> Figure:

        figure, axis = plt.subplots(figsize=figsize)

        colors = sns.color_palette("viridis", n_colors=len(df))

        bars = axis.barh(
            df["banks"],
            df["valor_indicador"],
            color=colors
        )

        self.add_value_labels(axis, bars, horizontal=True)

        axis.set_xlabel(f"Valor del Indicador({self.unit})", fontsize=11,
                        fontweight="bold")

        axis.set_title(title, fontsize=14, fontweight='bold', pad=20)
        axis.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        
        return figure


    def create_heatmap(
        self,
        pivot_df: pd.DataFrame,
        title,
        figsize: Tuple[int, int] = (12, 8),
        normalize: bool = True
    ):

        figure, axis = plt.subplots(figsize=figsize)

        data = pivot_df.copy()

        if normalize:

            data = data.div(data.max(axis=0), axis=1)

        sns.heatmap(
            data.T,
            annot=False,
            cmap="RdYlGn",
            cbar_kws={"label": "Valor Normalizado (0-1)" if normalize else "Valor"},
            ax=axis,
            linewidths=0.5
        )

        axis.set_title(title, fontsize=14, fontweight='bold', pad=20)
        axis.set_xlabel("Bancos", fontsize=11, fontweight='bold')
        axis.set_ylabel("Indicadores", fontsize=11, fontweight='bold')
        plt.tight_layout()

        return figure
