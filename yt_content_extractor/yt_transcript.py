from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import datetime
from pytube import YouTube


def write_transcript(url):
    id = url[17:]
    print(id)
    srt = YouTubeTranscriptApi.get_transcript(id)
    df = pd.DataFrame.from_dict(srt).sort_values(by = 'start')
    df['end'] = df['start'] + df['duration']
    df['start'] = df['start'].apply(lambda x: str(datetime.timedelta(seconds=x)))
    df['end'] = df['end'].apply(lambda x: str(datetime.timedelta(seconds=x)))
    video = YouTube(url)
    df.to_csv(str(video.title)+'.csv')



if __name__ == '__main__':
    write_transcript('https://youtu.be/4EtN3DM74Ko')