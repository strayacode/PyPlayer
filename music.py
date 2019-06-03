from tkinter import *
import os
import pygame
font = "inconsolata"
root = Tk()
root.minsize(800, 500)
pygame.mixer.init()
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

def play_pause_control():
	global state
	global played
	if state == "paused":
		if played == False:
			pygame.mixer.music.play()
			played = True
			state = "playing"
		elif played == True:
			pygame.mixer.music.unpause()
			state = "playing"
	elif state == "playing":
		if played == True:
			pygame.mixer.music.pause()
			state = "paused"

def previous_song():
	global index
	index -= 1
	if index == len(files):
		index = 0
	if index < 0:
		index = len(files) - 1
	pygame.mixer.music.load(files[index])
	pygame.mixer.music.play()

def next_song():
	global index
	index += 1
	if index == len(files):
		index = 0
	if index < 0:
		index = len(files) - 1
	pygame.mixer.music.load(files[index])	
	pygame.mixer.music.play()



# Placing widgets
songs = Listbox(root, width=100, font="{} 12".format(font))
songs.bind("<<ListboxSelect>>", songselect)
for song in files:
	songs.insert(END, song)
songs.place(x=0, y=0)
next_button = Button(root, width=10, text="Next", command=next_song, font="{} 12".format(font))
next_button.place(x=0, y=300)
play_button = Button(root, width=10, text="Play", command=play_pause_control, font="{} 12".format(font))
play_button.place(x=100, y=300)
previous_button = Button(root, width=10, text="Previous", command=previous_song, font="{} 12".format(font))
previous_button.place(x=200, y=300)
root.mainloop()