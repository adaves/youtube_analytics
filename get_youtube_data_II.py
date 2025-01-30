# get_youtube_data

import os
import pandas as pd
from googleapiclient.discovery import build
import json
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("YOUTUBE_API_KEY")
if not api_key:
    raise ValueError("YOUTUBE_API_KEY not found in environment variables")

# a list of channels to get data on
channels_list = ['schafer5', 'sentdex']

# initialize youtube object for api requests
youtube = build('youtube', 'v3', developerKey=api_key)

class YouTubeAPIHandler:

    def __init__(self, youtube): # type: ignore
        self.youtube = youtube

    def get_video_stats(self, usernames): # type: ignore
        """
        Calls youtube's API and makes a request, gets a response and loads that response into a dictionary

        Args:
            usernames (list): A list of usernames for youtube channels, these will be used by the API to get data.

        Returns:
            list: List of dictionaries containing channel data

        Raises:
            HttpError: If there's an API-related error
            ValueError: If usernames is empty or not a list
            Exception: For other unexpected errors
        """
        if not usernames or not isinstance(usernames, list):
            raise ValueError("usernames must be a non-empty list")

        channel_data = []

        # using nested try/except blocks to handle errors
        # the outer try/except catches general errors
        try:
            for username in usernames:

                # The inner try/except block catches errors specific to the API request
                try:
                    # make a request from youtube api
                    request = self.youtube.channels().list(
                        part='statistics',
                        forUsername=username
                    )

                    # response from youtube api
                    response = request.execute()

                    # code for debugging
                    print(f"API response = {json.dumps(response, indent=4, sort_keys=False)}")

                    if 'items' in response and len(response['items']) > 0:
                        stats = response['items'][0]['statistics']  # Extract statistics
                        channel_data.append({'username': username, **stats}) # add data to list, unpack stats into new dict
                    else:
                        print(f"Warning: No data found for username: {username}")

                except HttpError as e:
                    print(f"API error for username {username}: {e}")
                    continue

            if not channel_data:
                raise ValueError("No valid data was retrieved for any username")

            return channel_data

        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")
    
    def save_to_csv(self, channel_data, filename='channel_statistics.csv'): # type: ignore
        """
        Saves youtube channel statistics data to a csv file

        Args:
            channel_data (list): A list of dictionaries containing channel stats
            filename (str): The name of the output csv file

        Raises:
            ValueError: If channel_data is empty or invalid
            PermissionError: If file cannot be written due to permissions
            Exception: For other unexpected errors
        """
        if not channel_data or not isinstance(channel_data, list):
            raise ValueError("channel_data must be a non-empty list of dictionaries")

        try:
            df = pd.DataFrame(channel_data)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            df.to_csv(filename, index=False)
            print(f'Data successfully saved to {filename}')

        except PermissionError:
            raise PermissionError(f"Permission denied when writing to {filename}")
        except pd.errors.EmptyDataError:
            raise ValueError("Cannot save empty data to CSV")
        except Exception as e:
            raise Exception(f"Error saving data to CSV: {e}")

if __name__ == "__main__":

    # instantiate a an object for collecting data with the api
    yt = YouTubeAPIHandler(youtube)
    # call the get video stats function on the object
    channel_statistics = yt.get_video_stats(channels_list)
    # save the data to a csv file
    yt.save_to_csv(channel_statistics)

    for channel in channel_statistics:
        print(f"Channel: {channel['username']}, Statistics: {channel['statistics']}")

