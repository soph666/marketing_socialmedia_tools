from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import datetime
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import datetime
from pytube import YouTube
# from __future__ import unicode_literals
import youtube_dl
from random import random
import time
import sys
import os
import copy


def write_transcript(url):
    transcript = YouTubeTranscriptApi.get_transcript(url[17:])
    df = pd.DataFrame.from_dict(transcript).sort_values(by="start")
    df["end"] = df["start"] + df["duration"]
    df["start"] = df["start"].apply(lambda x: str(datetime.timedelta(seconds=x)))
    df["end"] = df["end"].apply(lambda x: str(datetime.timedelta(seconds=x)))
    video = YouTube(url)
    df.to_csv(sys.path[-2][:45]+'Data/'+str(video.title) + ".csv")

def yt_dl(urls):
    video = YouTube(urls)
    urls_list = copy.copy(urls)
    u = urls_list.split('/')[-1]
    print(''.join(video.title))
    ydl_opts = {'format': 'mp4'}
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     ydl.download([urls])
    if os.path.exists(os.path.dirname(os.path.abspath(__file__))+"/"+video.title+"-"+u+".mp4"):
        print('cp '+video.title+"-" +u+".mp4" + " "+sys.path[-2][:45]+"Data")
        os.system('cp ' + ''.join(video.title) + "-" + u + ".mp4" + " " + sys.path[-2][:45]+"Data")



# def yt_dl(url):
#     video = YouTube(url)
#     ydl_opts = {"format": "mp4"}
#     print(video.title)
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download(url)
#     print('done')
#     # mp4files = video.streams.filter(file_extension='mp4').get_highest_resolution()
    # print(mp4files)
    # video.set_filename(video.title)
    # stream = mp4files.streams.get_highest_resolution()
    # mp4files.download(output_path=sys.path[-1][:42]+'Data/', filename=mp4files.title)
    # d_video = video.get(mp4files[-1].extension, mp4files[-1].resolution)
    # try:
    #     d_video.download(sys.path[-1][:42]+'Data/')
    # except:
    #     print("Some Error!")
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     ydl.download(url)

# def run(urls):
#     write_transcript(urls)
#     yt_dl(urls)

def cuts_set(path):
    tspt = pd.read_csv(path)
    tspt["ind"] = tspt["ind"].apply(lambda x: True if x == "TRUE" else False)
    tspt["end"] = tspt["start"].shift(-1)
    tspt = tspt[tspt["ind"] == True]
    tspt = tspt[["start", "end", "ind"]]
    row = 0
    cuts = []
    while row < len(tspt.index) - 1:
        checkrow = row + 1
        ending = tspt["end"].iloc[row]
        while checkrow < len(tspt.index) - 1:
            if tspt["end"].iloc[checkrow] == tspt["start"].iloc[checkrow + 1]:
                ending = tspt["end"].iloc[checkrow]
                checkrow = checkrow + 1
                continue
            else:
                checkrow = checkrow + 1
                break
        cuts.append((tspt["start"].iloc[row], tspt["end"].iloc[checkrow - 1]))
        row = checkrow
    return cuts





def make_cuts(cuts, vid_path):
    video = VideoFileClip(vid_path)
    for cut in cuts:
        start = time.strptime(cut[0].split(",")[0], "%H:%M:%S")
        datetime.timedelta(
            hours=start.tm_hour, minutes=start.tm_min, seconds=start.tm_sec
        ).total_seconds()
        end = time.strptime(cut[0].split(",")[0], "%H:%M:%S")
        datetime.timedelta(
            hours=end.tm_hour, minutes=end.tm_min, seconds=end.tm_sec
        ).total_seconds()
        video.subclip(start, end)
        video.write_videofile(str(random()) + vid_path, fps=25)


if __name__ == "__main__":
    write_transcript("https://youtu.be/C1cEWlhMz0w")
    yt_dl("https://youtu.be/C1cEWlhMz0w")
