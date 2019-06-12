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

sc_opts = {
	'format': "http_mp3_128_url",
	'outtmpl': '/home/straya/snd/%(title)s.%(ext)s',
	'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3'
    }]
}

def download(term, service):
	if service == "Youtube":
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			if term.startswith('https://www.youtube.com/watch?v='):
				ydl.download([term])
			else:
				ydl.download(["ytsearch:{}".format(term)])
	if service == "Soundcloud":
		with youtube_dl.YoutubeDL(sc_opts) as sc:
			if term.startswith('https://soundcloud.com/'):
				sc.download([term])
			else:
				sc.download(["scsearch:{}".format(term)])