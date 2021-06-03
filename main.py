from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from youtubeTime import *

load_dotenv()
api_key = os.environ['api_key']

vid_len = []

youtubeService = build('youtube', 'v3', developerKey = api_key)

nextPageToken = None
while True:
    pl_request = youtubeService.playlistItems().list(
        part = 'contentDetails',
        playlistId = 'PLFs4vir_WsTwEd-nJgVJCZPNL3HALHHpF',
        maxResults = 500,
        pageToken = nextPageToken
    )
    pl_response = pl_request.execute()

    videos = []
    for item in pl_response['items']:
        videos.append(item['contentDetails']['videoId'])

    videos_request = youtubeService.videos().list(
        part = 'contentDetails',
        id = ','.join(videos)
    )
    videos_response = videos_request.execute()

    temp = ''
    for items in videos_response['items']:
        temp = items['contentDetails']['duration']
        timeObj = parseYTstring(temp)
        vid_len.append(getSeconds(timeObj['h'], timeObj['m'], timeObj['s']))

    nextPageToken = pl_response.get('nextPageToken')

    if not nextPageToken:
        break

totLen = gethms(sum(vid_len))


print(totLen)
print(faster(totLen, 1.25))
youtubeService.close()