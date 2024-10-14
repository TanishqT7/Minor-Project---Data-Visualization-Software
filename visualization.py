import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_scatter(data: pd.DataFrame, x_col: str, y_col: str, hue: str=None, title: str=None):

    plt.figure(figsize=(8,6))
    sns.scatterplot(data=data, x=x_col, y=y_col, hue=hue)
    
    plt.title(title or f"{x_col} vs. {y_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.legend(title=hue)
    plt.grid(True)
    plt.show()

def plot_histogram(data: pd.DataFrame, columns: str, bins: int=10, title: str=None):

    plt.figure(figsize=(8,6))
    sns.histplot(data[columns], bins=bins, kde=True)
    
    plt.title(title or f"Histogram of {columns}")
    plt.xlabel(columns)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

def plot_boxplot(data:pd.DataFrame, x_col: str, y_col: str=None, title: str=None):

    plt.figure(figsize=(8,6))
    sns.boxplot(data=data, x=x_col, y=y_col)
    
    plt.title(title or f"Boxplot of {x_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.grid(True)
    plt.show()