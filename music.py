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
os.chdir(path)
for (dirpath, dirnames, filenames) in os.walk(path):
	for c in range(0, len(filenames)):
		if filenames[c].endswith(".mp3"):
			files.append(filenames[c])
index = 0
pygame.mixer.music.load(files[index])

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
	songs.event_generate("<<ListboxSelect>>")
	

def next_song():
	global index
	global state
	global played
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
	songs.event_generate("<<ListboxSelect>>")

def thing(event):
	position_slider.bind("<ButtonRelease-1>", change_position)

def change_position(event):
	global index
	length = MP3(files[index]).info.length
	pygame.mixer.music.set_pos(length / (100 / position_slider.get()))




# Placing widgets
position_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=thing)
position_slider.place(x=0, y=450)
dynamic_control = StringVar()
dynamic_control.set("Play")
dynamic_title = StringVar()
song_title = Label(root, font="{} 12 bold".format(font), textvariable=dynamic_title, background="#191919", foreground="#ffffff")
song_title.place(x=0, y=400)
songs = Listbox(root, width=95, font="{} 12 bold".format(font), background="#191919", foreground="#ffffff", highlightthickness=0, borderwidth=-1,selectborderwidth=0, selectbackground="#639fff", selectforeground="#ffffff", relief=FLAT)
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

root.mainloop()
