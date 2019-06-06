from tkinter import *
import os
import pygame
from mutagen.mp3 import *
import math
font = "roboto"
root = Tk()
root.minsize(800, 500)
pygame.mixer.init()
root.configure(background="#191919")
files = []
path = "/home/straya/Downloads/"
played = False
state = "paused"
duration = 0
x_coord = 0
counter = 0
os.chdir(path)
for (dirpath, dirnames, filenames) in os.walk(path):
	for c in range(0, len(filenames)):
		if filenames[c].endswith(".mp3"):
			files.append(filenames[c])
index = 0
pygame.mixer.music.load(files[index])
import time

def songselect(event):
	index = songs.curselection()
	index = index[0]
	pygame.mixer.music.load(files[index])
	pygame.mixer.music.play()
	played = True
	state = "playing"
	dynamic_title.set(files[index][:-4])
	dynamic_control.set("Pause")

def play_pause_control():
	global state
	global played
	if state == "paused":
		if played == False:
			pygame.mixer.music.play()
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
	dynamic_title.set(files[index][:-4])
	state = "playing"
	played = True
	dynamic_control.set("Pause")
	if index == len(files) - 1:
		songs.select_clear(0)
	else:
		songs.select_clear(index + 1)
	songs.select_set(index)
	position_slider.set(0)
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
	
	songs.event_generate("<<ListboxSelect>>")

def thing(event):
	position_slider.bind("<Button-1>", mouse_click)

def check_duration():
	global index
	global duration
	global played
	global x_coord
	global counter
	length = MP3(files[index]).info.length
	

	formatted_length = time.strftime("%M:%S", time.gmtime(round(length, 1)))
	song_length.set(formatted_length)


	if state == "playing":
		counter += 0.1
		duration += round(10 / length, 2)
		x_coord += round(10 / length, 2)
		formatted_duration= time.strftime("%M:%S", time.gmtime(counter))
		current_pos.set(formatted_duration)
		position_slider.set(x_coord)
		print(round(length, 1), round(counter, 1))
		if round(length, 1) == round(counter, 1):
			next_song()
			duration = 0
			print("test")

	root.after(100, check_duration)

	
	

def mouse_click(event):
	global index
	global duration
	global x_coord
	global played
	global counter
	length = MP3(files[index]).info.length
	x_coord = 100 / (796 / event.x)
	position_slider.set(x_coord)
	if played == True:
		pygame.mixer.music.set_pos((length * x_coord) / 100)
		duration = round((length * x_coord) / 100, 1)
		counter = round((length * x_coord) / 100, 1)
	else:
		pygame.mixer.music.play()
		
	



# Placing widgets
position_slider = Scale(root, 
	from_=0, 
	to=100, 
	orient=HORIZONTAL, 
	command=thing, 
	background="#191919", 
	sliderrelief=FLAT, 
	sliderlength=5,
	relief=FLAT, 
	length=796, 
	troughcolor="#000000", 
	resolution=0.01, 
	showvalue=0,
	highlightbackground="#191919")
position_slider.place(x=0, y=450)
current_pos = StringVar()
song_length = StringVar()
dynamic_control = StringVar()
dynamic_control.set("Play")
dynamic_title = StringVar()
song_length_label = Label(root, font="{} 12 bold".format(font), textvariable=song_length, background="#191919", foreground="#ffffff")
current_pos_label = Label(root, font="{} 12 bold".format(font), textvariable=current_pos, background="#191919", foreground="#ffffff")
song_title = Label(root, font="{} 12 bold".format(font), textvariable=dynamic_title, background="#191919", foreground="#ffffff")
song_title.place(x=0, y=400)
songs = Listbox(root, width=95, font="{} 12 bold".format(font), background="#191919", foreground="#ffffff", highlightthickness=0, borderwidth=-1,selectborderwidth=0, selectbackground="#2d5391", selectforeground="#ffffff", relief=FLAT)
songs.bind("<<ListboxSelect>>", songselect)
for song in files:
	songs.insert(END, song)
songs.place(x=20, y=20)
next_button = Button(root, width=10, text="Next", command=next_song, font="{} 12".format(font))
next_button.place(x=0, y=300)
play_button = Button(root, width=10, text="Play", command=play_pause_control, font="{} 12".format(font), textvariable=dynamic_control)
play_button.place(x=100, y=300)
previous_button = Button(root, width=10, text="Previous", command=previous_song, font="{} 12".format(font))
previous_button.place(x=200, y=300)
song_length_label.place(x=750, y=420)
current_pos_label.place(x=0, y=420)
check_duration()
root.mainloop()