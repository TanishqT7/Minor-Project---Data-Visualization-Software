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

def plot_count(data:pd.DataFrame, column: str, title: str = None):
    plt.figure(figsize=(8,6))
    sns.countplot(data=data, x=column)
    plt.title(title or f"Count Plot of {column}")
    plt.xlabel(column)
    plt.ylabel('Count')
    plt.grid(True)
    plt.show()

def plot_pair(data:pd.DataFrame, hue:str = None):
    sns.pairplot(data, hue=hue)
    plt.show()

def plot_heatmap(data:pd.DataFrame):
    plt.figure(figsize=(8,6))
    corr = data.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.show()

def plot_violin(data: pd.DataFrame, x_col: str, y_col:str):
    plt.figure(figsize=(8,6))
    sns.violinplot(data=data, x=x_col, y=y_col)
    plt.title(f"Violin Plot of {x_col} vs {y_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.grid(True)
    plt.show()