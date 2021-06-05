from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import youtubeTime


load_dotenv()
api_key = os.environ['api_key']


def playlistLength(link):
    vid_len = []
    if '=' in link:
        link = link[link.index('=')+1:]
    youtubeService = build('youtube', 'v3', developerKey = api_key)

    nextPageToken = None
    while True:
        pl_request = youtubeService.playlistItems().list(
            part = 'contentDetails',
            playlistId = link,
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
            timeObj = youtubeTime.parseYTstring(temp)
            vid_len.append(youtubeTime.getSeconds(timeObj['h'], timeObj['m'], timeObj['s']))

        nextPageToken = pl_response.get('nextPageToken')

        if not nextPageToken:
            break

    totLen_sec = sum(vid_len)
    totLen_hms = youtubeTime.gethms(totLen_sec)
    play_len = len(vid_len)
    totLen_hms['n'] = play_len
    youtubeService.close()

    return totLen_hms

def faster(hms, speed):
    seconds = youtubeTime.getSeconds(int(hms['h']), int(hms['m']), int(hms['s']))
    reqtime = seconds / speed
    reqtime = youtubeTime.gethms(reqtime)
    return reqtime
    