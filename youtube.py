# get_youtube_data

import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


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

def visualize_viewCount(df) -> plt.Figure:
    """
    This functions plots the data from the `viewCount` column.

    Args:
        The dataframe containing the data.
    Returns:
        None
    """
    fig, ax = plt.subplots(figsize=(6,4))
    df.plot(kind='bar', y='viewCount', ax=ax)
    plt.xlabel('Username')
    plt.ylabel('View Count')
    plt.title('View Counts by Username')
    plt.xticks(ticks=range(len(df)), 
               labels=df['username'], 
               rotation=45, 
               ha='right')
    plt.tight_layout()
    
    return fig

def visualize_subscriberCount(df) -> plt.Figure:
    """
    This functions plots the data from the `subsciberCount` column.

    Args:
        The dataframe containing the data.
    Returns:
        None
    """
    fig, ax = plt.subplots(figsize=(6,4))
    df.plot(kind='bar', y='subscriberCount', ax=ax)
    plt.xlabel('Username')
    plt.ylabel('Subscriber Count')
    plt.title('Subscriber Counts by Username')
    plt.xticks(ticks=range(len(df)), 
               labels=df['username'], 
               rotation=45, 
               ha='right')
    plt.tight_layout()
    
    return fig

def views_vs_subscribers(df) -> plt.Figure:
    """
    this function is dumb, replace it...
    """
    fig, ax = plt.subplots(figsize=(8,6))
    df.plot(kind='scatter', x='subscriberCount', y='viewCount', ax=ax)
    plt.xlabel('Subscriber count')
    plt.ylabel('View count')
    plt.tight_layout()

    return fig


if __name__ == '__main__':
    df = load_data()

    print(df)

    fig1 = visualize_viewCount(df)
    fig2 = visualize_subscriberCount(df)
    fig3 = views_vs_subscribers(df)
    plt.show()