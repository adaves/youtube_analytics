# get_youtube_data

import os
import pandas as pd
from googleapiclient.discovery import build
import json

api_key = os.getenv("YOUTUBE_API_KEY")

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
            channel_data (dictionary): holds the retrieved data.
        """
        # save the channel data
        channel_data = []

        for username in usernames:
            # make a request from youtube api
            request = youtube.channels().list(
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
                    print(f"No data found for username: {username}")

            # stats = response['items'][0]['statistics']
            # channel_data.append({'username':username, 'statistics':stats})

        return channel_data
    
    def save_to_csv(self, channel_data, filename='channel_statistics.csv'): # type: ignore
        """
        Saves youtube channel statistics data to a csv file

        Args:
            channel_data(list): A list of dictionaries containing channel stats.

            filename (str): The name of the output csv file.

        Returns: 
            None
        """
        df = pd.DataFrame(channel_data)

        df.to_csv(filename, index=False)

        print(f'Data successfully saved to {filename}')
    

if __name__ == "__main__":

    # instantiate a an object for collecting data with the api
    yt = YouTubeAPIHandler(youtube)
    # call the get video stats function on the object
    channel_statistics = yt.get_video_stats(channels_list)
    # save the data to a csv file
    yt.save_to_csv(channel_statistics)

    for channel in channel_statistics:
        print(f"Channel: {channel['username']}, Statistics: {channel['statistics']}")

