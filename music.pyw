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
font = "roboto"
root = Tk()
root.minsize(950, 518)
pygame.mixer.init()
files = []
played = False
state = "paused"
repeat = False
duration = 0
x_coord = 0
counter = 0
data = {
	"AUDIO_DIR": "",
	"CODE_DIR" : "/home/straya/code/PyPlayer"
}


def get_directory():
	global data
	if len(data["AUDIO_DIR"]) == 0:
		data["AUDIO_DIR"] = filedialog.askdirectory()

if os.path.getsize("/home/straya/code/PyPlayer/data.json") == 0:
	file = open("data.json", "w+")
	get_directory()
	json.dump(data, file, indent=4)
else:
	file = open("data.json", "r")
	data_file = json.load(file)
	data["AUDIO_DIR"] = data_file["AUDIO_DIR"]

pygame.mixer.music.set_volume(0.4)
os.chdir(data["AUDIO_DIR"])

def get_files():
	files.clear()
	for (dirpath, dirnames, filenames) in os.walk(data["AUDIO_DIR"]):
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
	global repeat
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
	get_thumbnail(files[index])

def play_pause_control():
	global state
	global played
	if state == "paused":
		if played == False:
			pygame.mixer.music.play()
			songs.select_set(index)
			play_button.configure(image=pauseicon)
			played = True
			state = "playing"
			dynamic_title.set(files[index][:-4])
		elif played == True:
			pygame.mixer.music.unpause()
			play_button.configure(image=pauseicon)
			state = "playing"
			dynamic_title.set(files[index][:-4])
	elif state == "playing":
		if played == True:
			pygame.mixer.music.pause()
			play_button.configure(image=playicon)
			state = "paused"

def previous_song():
	global index
	global state
	global played
	global counter
	global duration
	global x_coord
	global repeat
	if repeat == False:
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
		if index == len(files) - 1:
			songs.select_clear(0)
		else:
			songs.select_clear(index + 1)
		songs.select_set(index)
		position_slider.set(0)
		get_thumbnail(files[index])
		songs.event_generate("<<ListboxSelect>>")
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
	
def next_song():
	global index
	global state
	global played
	global duration
	global x_coord
	global counter
	global repeat
	if repeat == False:
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
		if index == 0:
			songs.select_clear(len(files) - 1)
		else:
			songs.select_clear(index - 1)
		songs.select_set(index)
		position_slider.set(0)
		get_thumbnail(files[index])
		songs.event_generate("<<ListboxSelect>>")
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

def shuffle_song():
	global index
	global duration
	global x_coord
	global counter
	global played
	global repeat
	if played == False:
		next_song()
		previous_song()
	c = 0
	if repeat == False:
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
	else:
		pygame.mixer.music.load(files[index])
		pygame.mixer.music.play()
		dynamic_title.set(files[index][:-4])
		while c < len(files):
			songs.select_clear(c)
			c += 1
		position_slider.set(0)
		get_thumbnail(files[index])
		duration = 0
		x_coord = 0
		counter = 0
	play_button.configure(image=pauseicon)

def check_duration():
	global index
	global duration
	global played
	global x_coord
	global counter
	if len(files) > 0:
		length = MP3(files[index]).info.length
		formatted_length = time.strftime("/ %M:%S", time.gmtime(round(length, 1)))
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
	if pygame.mixer.music.get_pos() < 0:
		next_song()
		previous_song()
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
	global item
	length = MP3(files[index]).info.length
	x_coord = 100 / (950 / (event.x - 1))
	position_slider.set(x_coord)
	# canvas.move(item, x_coord, 2)
	if played == True:
		pygame.mixer.music.set_pos((length * x_coord) / 100)
		duration = round((length * x_coord) / 100, 1)
		counter = round((length * x_coord) / 100, 1)
	else:
		pygame.mixer.music.play()
		
def repeat_song():
	global repeat
	global repeat_state
	if repeat == False:
		repeat = True
		loop_button.configure(image=repeatonicon)
	else:
		repeat = False
		loop_button.configure(image=repeaticon)
	

def youtube_launch():
	def youtube_close():
		youtube_window.destroy()
		songs.delete(0, END)
		get_files()
		for file in files:
			songs.insert(END, "     " + file[:-4])
	
	youtube_window = Toplevel(background="#0c0c0c")
	youtube_window.geometry('800x500')
	style = ttk.Style()
	style.map('TCombobox', fieldbackground=[('readonly','#111111')])
	style.map('TCombobox', selectbackground=[('readonly','#111111')])
	style.map('TCombobox', background=[('readonly','#111111')])
	style.map('TCombobox', relief=[('readonly', 'flat')])
	style.map('TCombobox', shiftrelief=[('readonly', 'flat')])
	search_bar = Entry(youtube_window, font="{} 12 bold".format(font), width=78, foreground="#ffffff", background="#374089", highlightthickness=-1, bd=0)
	search_bar.place(x=0, y=440)
	def youtube_download():
		youtube.download(search_bar.get(), service_select.get())	
	close_button = Button(youtube_window, image=closeicon, command=youtube_close, background="#0c0c0c", activebackground="#0c0c0c", highlightthickness=-1, bd=0)
	close_button.place(x=752, y=-5)
	download_button = Button(youtube_window, image=downloadicon, command=youtube_download, background="#0c0c0c", activebackground="#0c0c0c", highlightthickness=-1, bd=0)
	download_button.place(x=730, y=440)

	service_select = ttk.Combobox(youtube_window, values=["Youtube", "Soundcloud"], font="{} 12 bold".format(font), state="readonly")
	service_select.place(x=0, y=470)

# Widget organisation
current_pos = StringVar()
song_length = StringVar()
dynamic_title = StringVar()
playicon = PhotoImage(file="{}/play_icon.png".format(data["CODE_DIR"]))
downloadicon = PhotoImage(file="{}/download_icon.png".format(data["CODE_DIR"]))
nexticon = PhotoImage(file="{}/next_icon.png".format(data["CODE_DIR"]))
previousicon = PhotoImage(file="{}/previous_icon.png".format(data["CODE_DIR"]))
shuffleicon = PhotoImage(file="{}/shuffle_icon.png".format(data["CODE_DIR"]))
pauseicon = PhotoImage(file="{}/pause_icon.png".format(data["CODE_DIR"]))
closeicon = PhotoImage(file="{}/close_icon.png".format(data["CODE_DIR"]))
circleicon = PhotoImage(file="{}/circle_icon.png".format(data["CODE_DIR"]))
repeatonicon = PhotoImage(file="{}/repeat_on_icon.png".format(data["CODE_DIR"]))
repeaticon = PhotoImage(file="{}/repeat_icon.png".format(data["CODE_DIR"]))
image = Image.open("/home/straya/snd/image.jpg")
resize = image.resize((45, 45), Image.ANTIALIAS)
resize.save("/home/straya/snd/image.jpg")
thumb = ImageTk.PhotoImage(image)
canvas = Canvas(root, width=1100, height=600, bg="#0c0c0c")
download_button = Button(root, command=youtube_launch, image=downloadicon, background="#000000", activebackground="#000000", highlightthickness=-1, bd=0)
thumbnail = Label(root, image=thumb, background="#0c0c0c", activebackground="#0c0c0c", highlightthickness=-1, bd=0)
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
song_title = Label(root, font="{} 12 bold".format(font), textvariable=dynamic_title, background="#000000", foreground="#ffffff")
loop_button = Button(root, command=repeat_song, image=repeaticon, background="#000000", fg="#ffffff", activebackground="#374089", highlightthickness=-1, bd=0)
songs = Listbox(root, width=50, height=18, font="{} 12".format(font), background="#111111", foreground="#ffffff", highlightthickness=0, borderwidth=0, selectborderwidth=0, selectbackground="#374089", selectforeground="#ffffff", relief=FLAT, activestyle="none")
previous_button = Button(root, command=previous_song, image=previousicon, background="#000000", activebackground="#374089", highlightthickness=-1, bd=0)
play_button = Button(root, image=playicon, command=play_pause_control, background="#000000", activebackground="#374089", highlightthickness=-1, bd=0)
song_length_label = Label(root, font="{} 12 bold".format(font), textvariable=song_length, background="#000000", foreground="#ffffff")
current_pos_label = Label(root, font="{} 12 bold".format(font), textvariable=current_pos, background="#000000", foreground="#ffffff")
next_button = Button(root, command=next_song, background="#000000", image=nexticon, activebackground="#374089", highlightthickness=-1, bd=0)
shuffle_button = Button(root, command=shuffle_song, background="#000000", image=shuffleicon, activebackground="#374089", highlightthickness=-1, bd=0)
position_slider = Scale(root, 
	from_=0, 
	to=100, 
	orient=HORIZONTAL, 
	background="#ffffff", 
	sliderrelief=FLAT, 
	sliderlength=5,
	relief=FLAT, 
	length=952, 
	troughcolor="#374089", 
	resolution=0.01, 
	showvalue=0,
	width=10,
	highlightbackground="#000000",
	highlightthickness=-1,
	bd=0)

# Placing the widgets
canvas.create_rectangle(0, 420, 950, 518, fill="black")
canvas.place(x=-1, y=-1)
download_button.place(x=660, y=450)
thumbnail.place(x=22, y=447)
songs.bind("<<ListboxSelect>>", songselect)

for song in files:
	songs.insert(END, "     " + song[:-4])
position_slider.place(x=-2, y=411)
volume_slider.place(x=730, y=488)
position_slider.bind("<Button-1>", mouse_click)

if len(files) != 0:
	dynamic_title.set(files[index][:-4])
songs.place(x=250, y=0)
song_title.place(x=75, y=468)
shuffle_button.place(x=730, y=450)
loop_button.place(x=900, y=450)
next_button.place(x=860, y=450)
play_button.place(x=815, y=450)
previous_button.place(x=770, y=450)
song_length_label.place(x=120, y=445)
current_pos_label.place(x=75, y=445)
volume_slider.set(0.4)
get_thumbnail(files[index])
check_duration()
root.mainloop()