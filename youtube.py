# ydl1.py

# import modules
from __future__ import unicode_literals
import youtube_dl

# dictionary used for youtube download options
ydl_opts = {
	# get the thumbnail for the song
	'writethumbnail': True,

	# format code used to download song which is m4a
	'format': "140",

	# the directory which the song is downloaded to
	'outtmpl': '/home/straya/snd/%(title)s.%(ext)s',

	# options used after the song has been downloaded 
	'postprocessors': [
		# only extract the audio from the link and use the mp3 file extension
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        },

        # embeds the thumbnail internally in the song for saved disk space
        {'key': 'EmbedThumbnail'},
    ],
}

# dictionary used for soundcloud download options
sc_opts = {
	# get the thumbnail for the song
	'writethumbnail': True,

	# format code used to download song which is mp3 in highest possible quality
	'format': "http_mp3_128_url",

	# the directory which the song is downloaded to
	'outtmpl': '/home/straya/snd/%(title)s.%(ext)s',

	# options used after the song has been downloaded 
	'postprocessors': [
		# only extract the audio from the link and use the mp3 file extension
		{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	    },

	    # embeds the thumbnail internally in the song for saved disk space
	    {'key': 'EmbedThumbnail'},   
    ],
}

# function which is used by the main program to download music
def download(term, service):
	# check which service is being used
	if service == "Youtube":
		# use the download options that we have specified
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			# allow for the usage of link download
			if term.startswith('https://www.youtube.com/watch?v='):
				# download song
				ydl.download([term])
			# download with a search term instead and take the first result
			else:
				# download song
				ydl.download(["ytsearch:{}".format(term)])
	if service == "Soundcloud":
		# use the download options that we have specified
		with youtube_dl.YoutubeDL(sc_opts) as sc:
			# allow for the usage of link download
			if term.startswith('https://soundcloud.com/'):
				# download song
				sc.download([term])
			# download with a search term instead and take the first result
			else:
				# download song
				sc.download(["scsearch:{}".format(term)])
	