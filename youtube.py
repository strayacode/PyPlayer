# ydl1.py
from __future__ import unicode_literals
import youtube_dl
ydl_opts = {
	'format': "140",
	'outtmpl': '/home/straya/snd/%(title)s.%(ext)s',
	'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3'
    }]
}

def download(term):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(["ytsearch:{}".format(term)])