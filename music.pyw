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
from config import *
font = "roboto"
root = Tk()
root.minsize(1100, 600)
pygame.mixer.init()
files = []
path = ""
played = False
state = "paused"
duration = 0
x_coord = 0
counter = 0
pygame.mixer.music.set_volume(0.1)
def get_directory():
	global path
	if len(path) == 0:
		path = filedialog.askdirectory()


if os.path.getsize("/home/straya/code/PyPlayer/preferences.txt") == 0:
	file = open("preferences.txt", "a")
	get_directory()
	file.write(path)	
	file.close()	
else:
	file = open("preferences.txt", "r")
	for line in file:
		path = line

pygame.mixer.music.set_volume(0.4)
os.chdir(path)

def get_files():
	files.clear()
	for (dirpath, dirnames, filenames) in os.walk(path):
		for c in range(0, len(filenames)):
			if filenames[c].endswith(".mp3"):
				files.append(filenames[c])

get_files()				
index = 0
if len(files) == 0:
	print("add some songs!")
else:
	pygame.mixer.music.load(files[index])


def songselect(event):
	global played
	global state
	global counter 
	global duration
	global x_coord
	duration = 0
	x_coord = 0
	counter = 0
	position_slider.set(0)
	index = songs.curselection()
	index = index[0]
	pygame.mixer.music.load(files[index])
	pygame.mixer.music.play()
	played = True
	state = "playing"
	dynamic_title.set(files[index][:-4])
	dynamic_control.set("Pause")
	get_thumbnail(files[index])

def play_pause_control():
	global state
	global played
	if state == "paused":
		if played == False:
			pygame.mixer.music.play()
			songs.select_set(index)
			played = True
			state = "playing"
			dynamic_title.set(files[index][:-4])
			dynamic_control.set("Pause")
		elif played == True:
			pygame.mixer.music.unpause()
			state = "playing"
			dynamic_title.set(files[index][:-4])
			dynamic_control.set("Pause")
	elif state == "playing":
		if played == True:
			pygame.mixer.music.pause()
			state = "paused"
			dynamic_title.set("")
			dynamic_control.set("Play")

def previous_song():
	global index
	global state
	global played
	global counter
	global duration
	global x_coord
	x_coord = 0
	duration = 0
	counter = 0
	index -= 1
	if index == len(files):
		index = 0
	if index < 0:
		index = len(files) - 1
	pygame.mixer.music.load(files[index])
	pygame.mixer.music.play()
	
	state = "playing"
	played = True
	dynamic_control.set("Pause")
	if index == len(files) - 1:
		songs.select_clear(0)
	else:
		songs.select_clear(index + 1)
	songs.select_set(index)
	position_slider.set(0)
	get_thumbnail(files[index])
	songs.event_generate("<<ListboxSelect>>")
	

def next_song():
	global index
	global state
	global played
	global duration
	global x_coord
	global counter
	duration = 0
	counter = 0
	x_coord = 0
	index += 1
	if index == len(files):
		index = 0
	if index < 0:
		index = len(files) - 1
	pygame.mixer.music.load(files[index])	
	pygame.mixer.music.play()
	dynamic_title.set(files[index][:-4])
	state = "playing"
	played = True
	dynamic_control.set("Pause")
	if index == 0:
		songs.select_clear(len(files) - 1)
	else:
		songs.select_clear(index - 1)
	songs.select_set(index)
	position_slider.set(0)
	get_thumbnail(files[index])
	songs.event_generate("<<ListboxSelect>>")

def shuffle_song():
	global index
	global duration
	global x_coord
	global counter
	global played

	if played == False:
		next_song()
		previous_song()
	c = 0
	random_song = (random.randint(0, len(files) - 1))
	index = random_song
	pygame.mixer.music.load(files[random_song])
	pygame.mixer.music.play()
	dynamic_title.set(files[random_song][:-4])
	while c < len(files):
		songs.select_clear(c)
		c += 1
	songs.select_set(random_song)
	position_slider.set(0)
	get_thumbnail(files[index])
	duration = 0
	x_coord = 0
	counter = 0

def thing(event):
	position_slider.bind("<Button-1>", mouse_click)

def check_duration():
	global index
	global duration
	global played
	global x_coord
	global counter

	if len(files) > 0:
		length = MP3(files[index]).info.length
		formatted_length = time.strftime("%M:%S", time.gmtime(round(length, 1)))
		song_length.set(formatted_length)
		if state == "paused" and played == False:
			current_pos.set("00:00")
		if state == "playing":
			counter += 0.1
			duration += round(10 / length, 2)
			x_coord += round(10 / length, 2)
			formatted_duration= time.strftime("%M:%S", time.gmtime(counter))
			current_pos.set(formatted_duration)
			position_slider.set(x_coord)
			if round(length, 1) == round(counter, 1):
				next_song()
				duration = 0
	root.after(100, check_duration)

def get_thumbnail(file):
	global thumbnail
	global thumb
	
	audio = ID3(file)
	album_art = audio.getall("APIC")[0].data
	with open("image.jpg", "wb") as img:
		img.write(album_art)
	thumb = Image.open("/home/straya/snd/image.jpg")
	resize = thumb.resize((45, 45), Image.ANTIALIAS)
	resize.save("/home/straya/snd/image.jpg")
	thumb_updated = ImageTk.PhotoImage(resize)
	thumbnail.configure(image=thumb_updated)
	thumbnail.image = thumb_updated
	
def volume(event):
	pygame.mixer.music.set_volume(volume_slider.get())	
	

def mouse_click(event):
	global index
	global duration
	global x_coord
	global played
	global counter
	length = MP3(files[index]).info.length
	x_coord = 100 / (1102 / (event.x - 1))
	position_slider.set(x_coord)
	if played == True:
		pygame.mixer.music.set_pos((length * x_coord) / 100)
		duration = round((length * x_coord) / 100, 1)
		counter = round((length * x_coord) / 100, 1)
	else:
		pygame.mixer.music.play()
		
def youtube_launch():
	def youtube_close():
		youtube_window.destroy()
		songs.delete(0, END)
		get_files()
		for file in files:
			songs.insert(END, file[:-4])
	
	youtube_window = Toplevel(background="#191919")
	youtube_window.geometry('800x500')
	search_bar = Entry(youtube_window, font="{} 12 bold".format(font), width=78)
	search_bar.place(x=0, y=0)
	def youtube_download():
		youtube.download(search_bar.get(), service_select.get())	
	close_button = Button(youtube_window, text="Close Window", font="{} 12 bold".format(font), command=youtube_close)
	close_button.place(x=300, y=400)
	download_button = Button(youtube_window, text="Download", font="{} 12 bold".format(font), command=youtube_download)
	download_button.place(x=705, y=0)
	service_select = ttk.Combobox(youtube_window, values=["Youtube", "Soundcloud"], font="{} 12 bold".format(font))
	service_select.place(x=0, y=200)






# Placing widgets
playicon = PhotoImage(file="{}/play_icon.png".format(PATH))
downloadicon = PhotoImage(file="{}/download_icon.png".format(PATH))
nexticon = PhotoImage(file="{}/next_icon.png".format(PATH))
previousicon = PhotoImage(file="{}/previous_icon.png".format(PATH))
shuffleicon = PhotoImage(file="{}/shuffle_icon.png".format(PATH))
pauseicon = PhotoImage(file="{}/pause_icon.png".format(PATH))
image = Image.open("/home/straya/snd/image.jpg")
resize = image.resize((45, 45), Image.ANTIALIAS)
resize.save("/home/straya/snd/image.jpg")
thumb = ImageTk.PhotoImage(resize)


canvas = Canvas(root, width=1100, height=600, bg="#111111")
canvas.create_rectangle(0, 530, 1100, 600, fill="black")
canvas.place(x=-1, y=-1)
download_button = Button(root, command=youtube_launch, image=downloadicon, background="#111111", activebackground="#111111", highlightthickness=-1, bd=0)
download_button.place(x=5, y=470)
thumbnail = Label(root, image=thumb)
thumbnail.place(x=6, y=544)
volume_slider = Scale(root, 
	from_=0, 
	to=1, 
	orient=HORIZONTAL,  
	background="#ffffff", 
	sliderrelief=FLAT, 
	sliderlength=5,
	width=10,
	relief=FLAT, 
	command=volume,
	length=200, 
	troughcolor="#374089", 
	resolution=0.01, 
	showvalue=0,
	highlightbackground="#000000",
	highlightthickness=-1,
	bd=0)

position_slider = Scale(root, 
	from_=0, 
	to=100, 
	orient=HORIZONTAL, 
	command=thing, 
	background="#ffffff", 
	sliderrelief=FLAT, 
	sliderlength=5,
	relief=FLAT, 
	length=1102, 
	troughcolor="#374089", 
	resolution=0.01, 
	showvalue=0,
	highlightbackground="#000000",
	highlightthickness=-1,
	bd=0)

position_slider.place(x=-2, y=520)
volume_slider.place(x=896, y=575)
current_pos = StringVar()
song_length = StringVar()
dynamic_control = StringVar()
dynamic_control.set("Play")
dynamic_title = StringVar()
if len(files) != 0:
	dynamic_title.set(files[index][:-4])
song_length_label = Label(root, font="{} 12 bold".format(font), textvariable=song_length, background="#000000", foreground="#ffffff")
current_pos_label = Label(root, font="{} 12 bold".format(font), textvariable=current_pos, background="#000000", foreground="#ffffff")
song_title = Label(root, font="{} 12 bold".format(font), textvariable=dynamic_title, background="#000000", foreground="#ffffff")
song_title.place(x=55, y=566)
songs = Listbox(root, width=50, font="{} 12 bold".format(font), background="#191919", foreground="#ffffff", highlightthickness=0, borderwidth=-1, selectborderwidth=0, selectbackground="#374089", selectforeground="#ffffff", relief=FLAT)
songs.bind("<<ListboxSelect>>", songselect)
for song in files:
	songs.insert(END, song[:-4])
shuffle_button = Button(root, command=shuffle_song, image=shuffleicon, background="#000000", activebackground="#374089", highlightthickness=-1, bd=0)
shuffle_button.place(x=400, y=540)
songs.place(x=20, y=20)
next_button = Button(root, command=next_song, background="#000000", image=nexticon, activebackground="#374089", highlightthickness=-1, bd=0)
next_button.place(x=550, y=540)
play_button = Button(root, image=playicon, command=play_pause_control, background="#000000", activebackground="#374089", highlightthickness=-1, bd=0)
play_button.place(x=500, y=540)
previous_button = Button(root, command=previous_song, image=previousicon, background="#000000", activebackground="#374089", highlightthickness=-1, bd=0)
previous_button.place(x=450, y=540)
song_length_label.place(x=1055, y=540)
current_pos_label.place(x=55, y=540)
volume_slider.set(0.4)
check_duration()
root.mainloop()