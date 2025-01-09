# get_youtube_data

import os
import zipfile
import pandas as pd
from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey = "AIzaSyD2tfLU0fP7hnnr-M5JVVboHZN3A7laozw")

request = youtube.channels().list(
    part='statistics',
    forUsername='schafer5'
    )

response = request.execute()

for key, value in response.items():
    print(f'key = {key}, value = {value}')
print()
print('Response = ', response['items'][0]['statistics'])

class GetYouTubeData:
    pass








# if __name__ == "__main__":