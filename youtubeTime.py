import re

def parseYTstring(vid):
    seconds_pattern = re.compile(r'(\d+)S')
    minutes_pattern = re.compile(r'(\d+)M')
    hours_pattern = re.compile(r'(\d+)H')

    h = 0, m = 0, s = 0

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


def faster(seconds, speed):
    reqtime = seconds / speed
    reqtime = gethms(reqtime)
    return reqtime
