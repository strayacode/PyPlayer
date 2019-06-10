# ydl1.py
from __future__ import unicode_literals
import youtube_dl
ydl_opts = {
	'audio-format': 'best',
	'outtmpl': 'D:/Documents/Music/%(title)s.%(ext)s',
	'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3'
    }]
}

def download(term):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(["ytsearch:{}".format(term)])