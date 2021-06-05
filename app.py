from flask import Flask, render_template, request, send_from_directory
import re
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
api_key = os.environ['api_key']

def parseYTstring(vid):
    seconds_pattern = re.compile(r'(\d+)S')
    minutes_pattern = re.compile(r'(\d+)M')
    hours_pattern = re.compile(r'(\d+)H')

    h = 0
    m = 0
    s = 0

    if seconds_pattern.search(vid):
        s = seconds_pattern.search(vid).group(1) 

    if minutes_pattern.search(vid):
        m = minutes_pattern.search(vid).group(1) 

    if hours_pattern.search(vid):
        h = hours_pattern.search(vid).group(1)    
    
    return {
                'h' : int(h),
                'm' : int(m),
                's' : int(s)
           }


def getSeconds(h, m, s):
    return h * 60 * 60 + m * 60 + s


def gethms(totalSeconds):
    temp = totalSeconds / (60 * 60)
    h = int(temp // 1)
    temp_m = temp%1 * 60
    m = int(temp_m // 1)
    s = int(round(temp_m % 1 * 60, 0))
    return {
        'h': int(h),
        'm': int(m),
        's': int(s)
    }


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
        if 'error' in pl_response:
            return -1
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

    totLen_sec = sum(vid_len)
    totLen_hms = gethms(totLen_sec)
    play_len = len(vid_len)
    totLen_hms['n'] = play_len
    youtubeService.close()

    return totLen_hms

def faster(hms, speed):
    seconds = getSeconds(int(hms['h']), int(hms['m']), int(hms['s']))
    reqtime = seconds / speed
    reqtime = gethms(reqtime)
    reqtime['n'] = hms['n']
    return reqtime


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def form_post():
    link = request.form['link']
    speed = float(request.form['speed'])
    time1x = playlistLength(link)
    if time1x == -1:
        return render_template('404.html')
    time = faster(time1x, speed)
    number = time['n']
    time = f"{time['h']} hours, {format(time['m'], '02d')} minutes and {format(time['s'], '02d')} seconds"
    final = f"This playlist has {number} videos."
    final2 = f"It would take you exactly {time} to watch the entire playlist at {speed}x speed."
    return render_template('index.html', final = final, final2 = final2)


@app.route('/youtube.svg') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'youtube.svg', mimetype='image/svg+xml')


if __name__ == '__main__':
    app.run()
