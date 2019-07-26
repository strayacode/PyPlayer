#!/usr/bin/python
# importing all the modules required for the program to function properly
from tkinter import *
from tkinter import filedialog, ttk
import os
import contextlib
with contextlib.redirect_stdout(None):
    import pygame 
from mutagen.mp3 import *
from mutagen.id3 import ID3
import math
import random
import youtube
from PIL import Image, ImageTk
import time
import json

# declaring all the variables required
font = "noto"
root = Tk()
root.minsize(950, 510)
pygame.mixer.init(22050, -16, 2, 2048)
files = []
queue_files = []
search_files = []
played = False
state = "paused"
repeat = False
duration = 0
x_coord = 0
counter = 0
index = 0
queue_index = 0 
mode = "all"
# dictionary used to specify music directory and code directory
data = {
	"AUDIO_DIR": "",
	"CODE_DIR" : "/home/straya/code/PyPlayer",
	"volume": 0.4
}


# function which is used to ask user for music directory if it has not been specified yet
def get_directory():
	global data
	if len(data["AUDIO_DIR"]) == 0:
		data["AUDIO_DIR"] = filedialog.askdirectory()

# write data dictonary to json file to be stored permanently
if os.path.getsize("/home/straya/code/PyPlayer/data.json") == 0:
	file = open("data.json", "w+")
	get_directory()
	json.dump(data, file, indent=4)

# if music directory already specified, load the data from the json file
else:
	file = open("{}/data.json".format(data["CODE_DIR"]), "r")
	data_file = json.load(file)
	data["AUDIO_DIR"] = data_file["AUDIO_DIR"]

# set the volume to be used for the music
pygame.mixer.music.set_volume(0.4)

# navigate to user-specified music directory
os.chdir(data["AUDIO_DIR"])

# function to find the files the music directory
def get_files():
	# clear files so that the songslist can update once a song has been downloaded
	files.clear()

	# find all files in directory
	for (dirpath, dirnames, filenames) in os.walk(data["AUDIO_DIR"]):
		for c in range(0, len(filenames)):
			# only append mp3 files to songslist
			if filenames[c].endswith(".mp3"):
				files.append(filenames[c])
# call function
get_files()				

# prompt user to add some songs if none are found
if len(files) == 0:
	print("add some songs!")
# load first song if songs are available
else:
	pygame.mixer.music.load(files[index])

def search_directory(event):
	global search_term
	search_files.clear()
	songs.delete(0, END)
	if search_bar.get() == "Search":
		search_bar.delete(0, END)
	if mode == "all":
		if len(search_bar.get()) == 0:
			if event.char == "":
				for song in files:
					songs.insert(END, "   " + song[:-4])
			else:
				if mode == "all":
					for song in files:
						if event.char.lower() in song.lower():
							songs.insert(END, "   " + song[:-4])
							search_files.append(song)
		else:
			if len(search_bar.get()) == 1 and event.char == "":
				for song in files:
					songs.insert(END, "   " + song[:-4])
			else:
				if mode == "all":
					for song in files:
						if search_bar.get().lower() in song.lower():
							songs.insert(END, "   " + song[:-4])
							search_files.append(song)
	if mode == "queue":
		if len(search_bar.get()) == 0:
			if event.char == "":
				for song in queue_files:
					songs.insert(END, "   " + song[:-4])
			else:
				if mode == "all":
					for song in queue_files:
						if event.char.lower() in song.lower():
							songs.insert(END, "   " + song[:-4])
							search_files.append(song)
		else:
			if len(search_bar.get()) == 1 and event.char == "":
				for song in queue_files:
					songs.insert(END, "   " + song[:-4])
			else:
				if mode == "all":
					for song in queue_files:
						if search_bar.get().lower() in song.lower():
							songs.insert(END, "   " + song[:-4])
							search_files.append(song)
def queue_add(event):
	add_index = songs.curselection()[0]
	if mode == "all":
		if len(search_files) == 0:
			queue_files.append(files[add_index])
			for c in range(0, len(files)):
				songs.select_clear(c)
			if len(queue_files) == 1:
				dynamic_queue.set("Queue - {} Track".format(len(queue_files)))
			else:
				dynamic_queue.set("Queue - {} Tracks".format(len(queue_files)))
		else:
			queue_files.append(search_files[add_index])
			for c in range(0, len(files)):
				songs.select_clear(c)
			if len(queue_files) == 1:
				dynamic_queue.set("Queue - {} Track".format(len(queue_files)))
			else:
				dynamic_queue.set("Queue - {} Tracks".format(len(queue_files)))
	elif mode == "queue":
		queue_files.pop(add_index)
		songs.delete(0, END)
		if len(queue_files) == 1:
			dynamic_queue.set("Queue - {} Track".format(len(queue_files)))
		elif len(queue_files) == 0:
			dynamic_queue.set("Queue")
			dynamic_status.set("Go add some songs to the queue!")
		else:
			dynamic_queue.set("Queue - {} Tracks".format(len(queue_files)))
		for song in queue_files:
			songs.insert(END, "   " + song[:-4])
		if len(queue_files) > 0:
			if queue_files[queue_index] == queue_files[add_index]:
				next_song()
				previous_song()


def display_queue():
	global mode
	if len(queue_files) == 0:
		dynamic_status.set("Go add some songs to the queue!")
		status_label.place(x=480, y=200)
	search_bar.delete(0, END)
	search_bar.insert(0, "Search")
	mode = "queue"
	songs.delete(0, END)
	for song in queue_files:
		songs.insert(END, "   " + song[:-4])


def display_all():
	global mode
	status_label.place_forget()
	dynamic_status.set("")
	search_bar.delete(0, END)
	search_bar.insert(0, "Search")
	mode = "all"
	songs.delete(0, END)
	for song in files:
		songs.insert(END, "   " + song[:-4])

# function which controls the state of playing or paused
def play_pause_control():
	# import local variables
	global state
	global played

	# check if song is paused
	if state == "paused":
		# check if a song has been played before
		if played == False:
			if len(queue_files) > 0:
				pygame.mixer.music.load(queue_files[queue_index])
				# play song
				pygame.mixer.music.play()

				# change play/pause icon to paused
				play_button.configure(image=pauseicon)

				# record that the song has been played and that the state is currently playing
				played = True
				state = "playing"

				# set song title to current song
				dynamic_title.set(queue_files[queue_index][:-4])
			else:
				# play song
				pygame.mixer.music.play()

				# change play/pause icon to paused
				play_button.configure(image=pauseicon)

				# record that the song has been played and that the state is currently playing
				played = True
				state = "playing"

				# set song title to current song
				dynamic_title.set(files[index][:-4])
		# call this if loop if a song has been played before, but it does the exact same thing
		elif played == True:
			if len(queue_files) > 0:
				pygame.mixer.music.unpause()
				play_button.configure(image=pauseicon)
				state = "playing"
				dynamic_title.set(queue_files[queue_index][:-4])
			else:
				pygame.mixer.music.unpause()
				play_button.configure(image=pauseicon)
				state = "playing"
				dynamic_title.set(files[index][:-4])
	# check if song is playing
	elif state == "playing":
		if played == True:
			# pause song
			pygame.mixer.music.pause()

			# change play/pause to play icon
			play_button.configure(image=playicon)

			# record the state to be paused
			state = "paused"

# function used to play the previous song
def previous_song():
	# import local variables
	global index
	global state
	global played
	global counter
	global duration
	global x_coord
	global repeat
	global queue_index

	if len(queue_files) > 0:
		# only play the previous song if repeat isn't on
		if repeat == False:
			# reset song length and position slider value to 0 
			x_coord = 0
			duration = 0
			counter = 0

			# change song index to the previous song
			queue_index -= 1

			# if the user goes to the previous song at index 0, play the last song in the list
			if queue_index < 0:
				queue_index = len(queue_files) - 1

			# play previous song
			pygame.mixer.music.load(queue_files[queue_index])
			pygame.mixer.music.play()

			# set the song title to the current song
			dynamic_title.set(queue_files[queue_index][:-4])

			# record that the song has been played and that the state is currently playing
			state = "playing"
			played = True
		
			# reset the position slider to 0
			position_slider.set(0)

			# set thumbnail to the current song
			get_thumbnail(queue_files[queue_index])

		# block of code instead if repeat is on which will just set the current position of the song to 0
		else:
			duration = 0
			counter = 0
			x_coord = 0
			pygame.mixer.music.load(queue_files[queue_index])	
			pygame.mixer.music.play()
			dynamic_title.set(queue_files[queue_index][:-4])
			state = "playing"
			played = True
			position_slider.set(0)
	else:
		# only play the previous song if repeat isn't on
		if repeat == False:
			# reset song length and position slider value to 0 
			x_coord = 0
			duration = 0
			counter = 0

			# change song index to the previous song
			index -= 1

			# if the user goes to the previous song at index 0, play the last song in the list
			if index < 0:
				index = len(files) - 1

			# play previous song
			pygame.mixer.music.load(files[index])
			pygame.mixer.music.play()

			# set the song title to the current song
			dynamic_title.set(files[index][:-4])

			# record that the song has been played and that the state is currently playing
			state = "playing"
			played = True

			# reset the position slider to 0
			position_slider.set(0)

			# set thumbnail to the current song
			get_thumbnail(files[index])

		# block of code instead if repeat is on which will just set the current position of the song to 0
		else:
			duration = 0
			counter = 0
			x_coord = 0
			pygame.mixer.music.load(files[index])	
			pygame.mixer.music.play()
			dynamic_title.set(files[index][:-4])
			state = "playing"
			played = True
			position_slider.set(0)

# function used to play the next song
def next_song():
	# import local variables
	global index
	global state
	global played
	global duration
	global x_coord
	global counter
	global repeat
	global queue_index
	if len(queue_files) > 0:
		# only play the previous song if repeat isn't on
		if repeat == False:
			# reset song length and position slider value to 0 
			duration = 0
			counter = 0
			x_coord = 0

			# change song index to the next song
			queue_index += 1

			# if the user goes to the next song on last song, play the first song in the list
			if queue_index == len(queue_files):
				queue_index = 0
			
			# play the next song
			pygame.mixer.music.load(queue_files[queue_index])	
			pygame.mixer.music.play()

			# set the song title to the current song
			dynamic_title.set(queue_files[queue_index][:-4])

			# record that the song has been played and that the state is currently playing
			state = "playing"
			played = True

			# set the position slider to 0
			position_slider.set(0)

			# set the thumbnail to the current
			get_thumbnail(queue_files[queue_index])

		# call this block of code instead if repeat is on which just resets the position of the song to 0
		else:
			duration = 0
			counter = 0
			x_coord = 0
			pygame.mixer.music.load(queue_files[index])	
			pygame.mixer.music.play()
			dynamic_title.set(queue_files[index][:-4])
			state = "playing"
			played = True
			position_slider.set(0)
		play_button.configure(image=pauseicon)
	else:
		# only play the previous song if repeat isn't on
		if repeat == False:
			# reset song length and position slider value to 0 
			duration = 0
			counter = 0
			x_coord = 0

			# change song index to the next song
			index += 1

			# if the user goes to the next song on last song, play the first song in the list
			if index == len(files):
				index = 0
		
			# play the next song
			pygame.mixer.music.load(files[index])	
			pygame.mixer.music.play()

			# set the song title to the current song
			dynamic_title.set(files[index][:-4])

			# record that the song has been played and that the state is currently playing
			state = "playing"
			played = True

			# set the thumbnail to the current
			get_thumbnail(files[index])

			# generate listboxselect event
			songs.event_generate("<<ListboxSelect>>")

		# call this block of code instead if repeat is on which just resets the position of the song to 0
		else:
			duration = 0
			counter = 0
			x_coord = 0
			pygame.mixer.music.load(files[index])	
			pygame.mixer.music.play()
			dynamic_title.set(files[index][:-4])
			state = "playing"
			played = True
			position_slider.set(0)
		play_button.configure(image=pauseicon)

# function to play a song randomly
def shuffle_song():
	# import local variables
	global index
	global duration
	global x_coord
	global counter
	global played
	global repeat
	global queue_index
	# code which will make sure song is played if one hasn't been played yet
	if played == False:
		next_song()
		previous_song()

	if len(queue_files) > 0:
		# if repeat is off normally shuffle song
		if repeat == False:
			# choose random song in song list
			random_song = (random.randint(0, len(queue_files) - 1))

			# change the song index to the random song index
			queue_index = random_song

			# play the random song
			pygame.mixer.music.load(queue_files[random_song])
			pygame.mixer.music.play()

			# set the song title to the random song
			dynamic_title.set(queue_files[random_song][:-4])

			# set the position slider to 0
			position_slider.set(0)

			# set the thumbnail to the current song
			get_thumbnail(queue_files[queue_index])

			# set song position values to 0
			duration = 0
			x_coord = 0
			counter = 0

		# call this block of code if repeat is on which just sets the song position of the song to 0
		else:
			pygame.mixer.music.load(queue_files[queue_index])
			pygame.mixer.music.play()
			dynamic_title.set(queue_files[queue_index][:-4])
			position_slider.set(0)
			get_thumbnail(queue_files[queue_index])
			duration = 0
			x_coord = 0
			counter = 0

		# set the play/pause icon to a pauseicon
		play_button.configure(image=pauseicon)

	else:
		# if repeat is off normally shuffle song
		if repeat == False:
			# choose random song in song list
			random_song = (random.randint(0, len(files) - 1))

			# change the song index to the random song index
			index = random_song

			# play the random song
			pygame.mixer.music.load(files[random_song])
			pygame.mixer.music.play()

			# set the song title to the random song
			dynamic_title.set(files[random_song][:-4])

			# set the position slider to 0
			position_slider.set(0)

			# set the thumbnail to the current song
			get_thumbnail(files[index])

			# set song position values to 0
			duration = 0
			x_coord = 0
			counter = 0

		# call this block of code if repeat is on which just sets the song position of the song to 0
		else:

			pygame.mixer.music.load(files[index])
			pygame.mixer.music.play()
			dynamic_title.set(files[index][:-4])
			position_slider.set(0)
			get_thumbnail(files[index])
			duration = 0
			x_coord = 0
			counter = 0

		# set the play/pause icon to a pauseicon
		play_button.configure(image=pauseicon)

# function which checks the current song position every 100 milliseconds
def check_duration():
	# import local variables 
	global index
	global duration
	global played
	global x_coord
	global counter

	if len(queue_files) > 0:
		# get the length for the current song
		length = MP3(queue_files[queue_index]).info.length

		# format the length which is in seconds into minutes and seconds
		formatted_length = time.strftime("/ %M:%S", time.gmtime(round(length, 1)))

		# change the song length label to the song length of the current song
		song_length.set(formatted_length)

		# if song has never been played before, set the current position label to 0
		if state == "paused" and played == False:
			current_pos.set("00:00")

		# if the song state is playing
		if state == "playing":
			# add 0.1 to the counter variable
			counter += 0.1

			# add 0.1 to the duration and the x coordinate of the position slider
			duration += round(10 / length, 2)
			x_coord += round(10 / length, 2)

			# format the current position which is in seconds to minutes and seconds
			formatted_duration= time.strftime("%M:%S", time.gmtime(counter))

			# set the current position length label to the current position of the current song
			current_pos.set(formatted_duration)

			# update the position of the position slider to the value of x_coord
			position_slider.set(x_coord)

			# check if the song has ended
			if round(length, 1) == round(counter, 1) or round(counter, 1) > round(length, 1):
				# play the next song
				next_song()
				# set the song position to 0
				duration = 0
	elif len(files) > 0:
		# get the length for the current song
		length = MP3(files[index]).info.length

		# format the length which is in seconds into minutes and seconds
		formatted_length = time.strftime("/ %M:%S", time.gmtime(round(length, 1)))

		# change the song length label to the song length of the current song
		song_length.set(formatted_length)

		# if song has never been played before, set the current position label to 0
		if state == "paused" and played == False:
			current_pos.set("00:00")

		# if the song state is playing
		if state == "playing":
			# add 0.1 to the counter variable
			counter += 0.1

			# add 0.1 to the duration and the x coordinate of the position slider
			duration += round(10 / length, 2)
			x_coord += round(10 / length, 2)

			# format the current position which is in seconds to minutes and seconds
			formatted_duration= time.strftime("%M:%S", time.gmtime(counter))

			# set the current position length label to the current position of the current song
			current_pos.set(formatted_duration)

			# update the position of the position slider to the value of x_coord
			position_slider.set(x_coord)

			# check if the song has ended
			if round(length, 1) == round(counter, 1) or round(counter, 1) > round(length, 1):
				# play the next song
				next_song()
				# set the song position to 0
				duration = 0
	
	# if statement which fixes bug where song would play without audio
	if played == True:
				# if song position is an invalid value
				if pygame.mixer.music.get_pos() < 0:
					# play the next song and then previous song to set the song position back to a valid value of 0
					next_song()
					previous_song()
			
	# call this function every 100 milliseconds		
	root.after(98, check_duration)

# function which is used to get the thumbnail of the current song, the argument file is also used to make the code more efficient in terms of lines of code
def get_thumbnail(file):
	# import local variables
	global thumbnail
	global thumb

	# convert the file to an ID3 object which can be used by mutagen to extract metadata
	audio = ID3(file)

	# extract the raw jpeg data of the thumbnail
	album_art = audio.getall("APIC")[0].data

	# use the already existing file image.jpg
	with open("image.jpg", "wb") as img:
		# write the contents of the jpeg data to image.jpg, changing the image seen in image.jpg
		img.write(album_art)

	# open the thumbnail for resizing use
	thumb = Image.open("/home/straya/snd/image.jpg")

	# resize the thumbnail to a 45x45 image
	resize = thumb.resize((50, 50), Image.ANTIALIAS)

	# save the resized image to image.jpg
	resize.save("/home/straya/snd/image.jpg")

	# load the thumbnail for widget use
	thumb_updated = ImageTk.PhotoImage(resize)

	# change the image of the image widget to the current thumbnail
	thumbnail.configure(image=thumb_updated)

	# keep a reference of the image so that the widget doesn't produce a blank image
	thumbnail.image = thumb_updated
	
# function used to change the volume of the song
def volume(event):
	# set the volume of the song to the value of the volume slider
	pygame.mixer.music.set_volume(volume_slider.get())
	if pygame.mixer.music.get_volume() != 0:
		data["volume"] = volume_slider.get()	
	
# function which changes the position of the song to the x coordinate of the position slider
def mouse_click(event):
	# import local variables
	global index
	global duration
	global x_coord
	global played
	global counter

	if len(queue_files) > 0:
		# get the current song length
		length = MP3(queue_files[queue_index]).info.length
	elif len(files) > 0:
		# get the current song length
		length = MP3(files[index]).info.length


	# convert the value of the x coordinate to a percentage out of 100
	x_coord = 100 / (954 / (event.x - 1))

	# set the position slider to be at the same value as the x coordinate
	position_slider.set(x_coord)

	# if statement to check if any music has been played
	if played == True:
		# set the actual song position to the length times the percentage
		pygame.mixer.music.set_pos((length * x_coord) / 100)

		# round both the duration and counter variables to 1 decimal place
		duration = round((length * x_coord) / 100, 1)
		counter = round((length * x_coord) / 100, 1)

	# play music normally if none has been played yet
	else:
		pygame.mixer.music.play()
	
# function used to toggle between repeat on and off		
def repeat_song():
	# import local variables
	global repeat
	global repeat_state

	# check if repeat is off
	if repeat == False:

		# set repeat on
		repeat = True

		# set the repeat icon to repeaton
		loop_button.configure(image=repeatonicon)

	# check if repeat is on
	else:

		# set repeat to false
		repeat = False

		# set the repeat icon to repeatoff
		loop_button.configure(image=repeaticon)
	
# function used to make the interface for downloading music
def youtube_launch():
	global mode
	# function used to close the music downloader window
	def youtube_close():
		mode = "all"
		# close music downloader window
		youtube_window.destroy()

		# remove all files in songs list
		songs.delete(0, END)

		# add the files back again which refreshes the songs with newly downloaded song
		get_files()

		# add padding to the songs list
		for file in files:
			songs.insert(END, "   " + file[:-4])
	
	# create the music downloader widget
	youtube_window = Toplevel(background="#0c0c0c")

	# change the window size to 800x500
	youtube_window.geometry('500x250')

	# make a new style
	style = ttk.Style()

	# theme the combobox widget 
	style.map('TCombobox', fieldbackground=[('readonly','#111111')])
	style.map('TCombobox', selectbackground=[('readonly','#111111')])
	style.map('TCombobox', background=[('readonly','#111111')])
	style.map('TCombobox', relief=[('readonly', 'flat')])
	style.map('TCombobox', shiftrelief=[('readonly', 'flat')])
	style.map('TCombobox', foreground=[('readonly', '#ffffff')])

	# create the search bar
	entry_var = StringVar()
	search_bar = Entry(youtube_window, font="{} 12 bold".format(font), textvariable=entry_var, width=45, foreground="#ffffff", background="#374089", highlightthickness=-1, bd=0)
	search_bar.place(x=5, y=190)

	download_label = Label(youtube_window, text="Downloads", font="{} 12 bold".format(font), bg="#111111", fg="#ffffff")
	download_label.place(x=0, y=0)
	
	# function used to download music
	def youtube_download():
		# call the download function from youtube.py supplying 2 arguments: the search term/link and the service
		youtube.download(search_bar.get(), service_select.get())

	# create the close button	
	close_button = Button(youtube_window, image=closeicon, command=youtube_close, background="#0c0c0c", activebackground="#0c0c0c", highlightthickness=-1, bd=0)
	close_button.place(x=452, y=-5)

	# create the download button
	download_button = Button(youtube_window, image=downloadicon, command=youtube_download, background="#0c0c0c", activebackground="#0c0c0c", highlightthickness=-1, bd=0)
	download_button.place(x=430, y=180)

	# create the service selector widget
	service_select = ttk.Combobox(youtube_window, values=["Youtube", "Soundcloud"], font="{} 11".format(font), state="readonly")
	service_select.place(x=5, y=220) 
	service_select.current(0)
	

def keylisten(event):
	global counter
	global x_coord
	global index
	if "entry" not in str(root.focus_get()):
		volume = volume_slider.get()
		length = MP3(files[index]).info.length
		if event.char == " ":
			play_pause_control()
		if counter >= 0:
			if event.keysym == "Right":
				counter += 10
				x_coord += round(1000 / length, 2)
				pygame.mixer.music.set_pos(counter)

			if event.keysym == "Left":
				if counter <= 10:
					counter = 0
					x_coord = 0
					pygame.mixer.music.set_pos(counter)
				else:
					counter -= 10
					x_coord -= round(1000 / length, 2)
					pygame.mixer.music.set_pos(counter)
		if event.char == "m":
			if pygame.mixer.music.get_volume() == 0:
				pygame.mixer.music.set_volume(data["volume"])
				volume_slider.set(data["volume"])
			else:
				pygame.mixer.music.set_volume(0)
				volume_slider.set(0)
		if event.char == "=":
			pygame.mixer.music.set_volume(volume + 0.05)
			volume_slider.set(volume + 0.05)
		if event.char == "-":
			pygame.mixer.music.set_volume(volume - 0.05)
			volume_slider.set(volume - 0.05)
		if event.char == ".":
			next_song()
		if event.char == ",":
			previous_song()
		if event.char == "s":
			shuffle_song()

# Widget organisation

# create the string variables
current_pos = StringVar()
song_length = StringVar()
dynamic_title = StringVar()
dynamic_queue = StringVar()
dynamic_status = StringVar()
dynamic_queue.set("Queue")
# load all the images required
playicon = PhotoImage(file="{}/play_icon.png".format(data["CODE_DIR"]))
downloadicon = PhotoImage(file="{}/download_icon.png".format(data["CODE_DIR"]))
nexticon = PhotoImage(file="{}/next_icon.png".format(data["CODE_DIR"]))
previousicon = PhotoImage(file="{}/previous_icon.png".format(data["CODE_DIR"]))
shuffleicon = PhotoImage(file="{}/shuffle_icon.png".format(data["CODE_DIR"]))
pauseicon = PhotoImage(file="{}/pause_icon.png".format(data["CODE_DIR"]))
closeicon = PhotoImage(file="{}/close_icon.png".format(data["CODE_DIR"]))
repeatonicon = PhotoImage(file="{}/repeat_on_icon.png".format(data["CODE_DIR"]))
repeaticon = PhotoImage(file="{}/repeat_icon.png".format(data["CODE_DIR"]))
searchicon = PhotoImage(file="{}/search_icon.png".format(data["CODE_DIR"]))

# resize the inital image for image.jpg
image = Image.open("/home/straya/snd/image.jpg")
resize = image.resize((50, 50), Image.ANTIALIAS)
resize.save("/home/straya/snd/image.jpg")
thumb = ImageTk.PhotoImage(image)

# create a canvas
canvas = Canvas(root, width=1100, height=600, bg="#0c0c0c")

# add the download button in the main window
download_button = Button(root, command=youtube_launch, image=downloadicon, background="#000000", activebackground="#000000", highlightthickness=-1, bd=0)

# create the thumbnail widget
thumbnail = Label(root, image=thumb, background="#0c0c0c", activebackground="#0c0c0c", highlightthickness=-1, bd=0)

# create the queue window button
queue_button = Button(root, width=25, command=display_queue, font="{} 10 bold".format(font), text="Queue", textvariable=dynamic_queue, fg="#8c8c8c", bg="#0c0c0c", activebackground="#0c0c0c", activeforeground="#ffffff", highlightthickness=-1, bd=0, anchor=W, relief="flat")
all_button = Button(root, width=25, command=display_all, font="{} 10 bold".format(font), text="All", fg="#8c8c8c", bg="#0c0c0c", activebackground="#0c0c0c", activeforeground="#ffffff", highlightthickness=-1, bd=0, anchor=W, relief="flat")
search_label = Label(root, image=searchicon)
# create the volume slider 
volume_slider = Scale(root, 
	from_=0, 
	to=1, 
	orient=HORIZONTAL,  
	background="#ffffff", 
	sliderrelief=FLAT, 
	sliderlength=5,
	width=8,
	relief=FLAT, 
	command=volume,
	length=200, 
	troughcolor="#636ec9", 
	resolution=0.01, 
	showvalue=0,
	highlightbackground="#000000",
	highlightthickness=-1,
	bd=0)

# create music control buttons and labels
song_title = Label(root, font="{} 10 bold".format(font), textvariable=dynamic_title, background="#000000", foreground="#ffffff")
loop_button = Button(root, command=repeat_song, image=repeaticon, background="#000000", fg="#ffffff", activebackground="#000000", highlightthickness=-1, bd=0)
songs = Listbox(root, width=95, height=21, font="{} 10".format(font), background="#111111", foreground="#ffffff", highlightthickness=0, borderwidth=0, selectborderwidth=0, selectbackground="#636ec9", selectforeground="#ffffff", relief=FLAT, activestyle="none")
previous_button = Button(root, command=previous_song, image=previousicon, background="#000000", activebackground="#000000", highlightthickness=-1, bd=0)
play_button = Button(root, image=playicon, command=play_pause_control, background="#000000", activebackground="#000000", highlightthickness=-1, bd=0)
song_length_label = Label(root, font="{} 11".format(font), textvariable=song_length, background="#000000", foreground="#ffffff")
current_pos_label = Label(root, font="{} 11".format(font), textvariable=current_pos, background="#000000", foreground="#ffffff")
next_button = Button(root, command=next_song, background="#000000", image=nexticon, activebackground="#000000", highlightthickness=-1, bd=0)
shuffle_button = Button(root, command=shuffle_song, background="#000000", image=shuffleicon, activebackground="#000000", highlightthickness=-1, bd=0)
search_bar = Entry(root, width=23, font="{} 11".format(font), highlightthickness=-1, bd=0, bg="#636ec9", fg="#ffffff")
status_label = Message(root, textvariable=dynamic_status, font="{} 13 bold".format(font), width=200, fg="#8c8c8c", bg="#111111", justify=CENTER)
# create position slider
position_slider = Scale(root, 
	from_=0, 
	to=100, 
	orient=HORIZONTAL, 
	background="#ffffff", 
	sliderrelief=FLAT, 
	sliderlength=5,
	relief=FLAT, 
	length=952, 
	troughcolor="#636ec9", 
	resolution=0.01, 
	showvalue=0,
	width=10,
	highlightbackground="#000000",
	highlightthickness=-1,
	bd=0)

# Placing the widgets
canvas.create_rectangle(0, 420, 950, 518, fill="#000000")

canvas.place(x=-1, y=-1)
download_button.place(x=660, y=450)
thumbnail.place(x=14, y=444)

# insert the songs into the song list at the start of the program
for song in files:
	songs.insert(END, "   " + song[:-4])
position_slider.place(x=0, y=420)
volume_slider.place(x=730, y=483)

# bind left mouse click to mouse click function
position_slider.bind("<Button-1>", mouse_click)

songs.bind("<Double-Button-1>", queue_add)
# set the song title label to the first song
if len(files) != 0:
	dynamic_title.set(files[index][:-4])
songs.place(x=194, y=0)
song_title.place(x=75, y=445)
shuffle_button.place(x=730, y=450)
loop_button.place(x=900, y=450)
next_button.place(x=860, y=450)
play_button.place(x=815, y=450)
previous_button.place(x=770, y=450)
song_length_label.place(x=120, y=469)
current_pos_label.place(x=75, y=469)
queue_button.place(x=-2, y=23)
all_button.place(x=-2, y=48)
canvas.create_rectangle(0, 0, 50, 24, fill="#636ec9")
# set the volume of the song
volume_slider.set(0.4)

# set the thumbnail of the current song
if len(files) > 0:
	get_thumbnail(files[index])

# call the check duration function
check_duration()
search_bar.insert(0, "Search")

search_bar.bind("<Key>", search_directory)
search_bar.bind("<Button-1>", search_directory)

search_bar.place(x=10, y=0)

root.bind("<Key>", keylisten)

# initialize the tkinter window
root.mainloop()
