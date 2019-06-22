# ydl1.py
from __future__ import unicode_literals
import youtube_dl
import json
file = open("data.json", "r")
data_file = json.load(file)


ydl_opts = {
	'writethumbnail': True,
	'format': "140",
	'outtmpl': '{}/%(title)s.%(ext)s'.format(data_file["AUDIO_DIR"]),
	'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        },
        {'key': 'EmbedThumbnail'},
    ],
}

sc_opts = {
	'writethumbnail': True,
	'format': "http_mp3_128_url",
	'outtmpl': '{}/%(title)s.%(ext)s'.format(data_file["AUDIO_DIR"]),
	'postprocessors': [
		{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	    },
	    {'key': 'EmbedThumbnail'},   
    ],
}

def download(term, service):
	try:
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
	except:
		print("No internet connection available")