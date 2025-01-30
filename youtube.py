        # get_youtube_data

import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data() -> pd.DataFrame:
    """
    This function loads the data from a csv into a Pandas dataframe.

    Returns:
    pd.DataFrame: A dataframe containing the data from the csv file.

    Raises:
    FileNotFoundError: If the csv file does not exist.
    pd.errors.EmptyDataError: If the csv file is empty.
    pr.errors.ParseError: If there is a parsing error while reading the csv file.
    """

    # Construct a dynamic file path to the script
    script_dir = Path(__file__).resolve().parent.parent

    # Construct a dynamic file path to the dataset
    data_path = "channel_statistics.csv"

    # Load the csv into a DataFrame with error handling
    try:            
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {data_path}")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(f"No data: {data_path}")
    except pd.errors.ParserError:
        raise pd.errors.ParserError(f"Parsing error: {data_path}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
    
    return df

def visualize_count(df, column: str) -> plt.Figure:
    """
    Creates a bar plot for the specified column from the dataframe.

    Args:
        df (pd.DataFrame): The dataframe containing the data
        column (str): The column to visualize ('viewCount', 'subscriberCount', or 'videoCount')

    Returns:
        plt.Figure: The generated plot figure
    """
    fig, ax = plt.subplots(figsize=(6,4))
    df.plot(kind='bar', y=column, ax=ax)
    plt.xlabel('Username')
    plt.ylabel(f'{column.replace("Count", " Count")}')
    plt.title(f'{column.replace("Count", " Count")}s by Username')
    plt.xticks(ticks=range(len(df)), 
               labels=df['username'], 
               rotation=45, 
               ha='right')
    plt.tight_layout()
    
    return fig

def correlation_heatmap(df) -> plt.Figure:
    """
    This function accepts a df parameter, and builds a heatmap showing data correlation

    Args:
        The dataframe containing the data

    Returns:
        A heatmap figure with data correlation values
    """
    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(df.select_dtypes(include=['float64', 'int64']).corr(), ax=ax)

    return fig



if __name__ == '__main__':
    df = load_data()
    df.drop(columns=['hiddenSubscriberCount'], inplace=True)
    print(df)

    fig1 = visualize_count(df, 'viewCount')
    fig2 = visualize_count(df, 'subscriberCount')
    fig3 = visualize_count(df, 'videoCount')
    fig4 = correlation_heatmap(df)

    plt.show()